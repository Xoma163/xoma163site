from datetime import datetime, timedelta, date

from django.core.management.base import BaseCommand

from apps.API_VK.VkEvent import VkEvent
from apps.service.models import Notify
from xoma163site.wsgi import vk_bot


class Command(BaseCommand):

    def handle(self, *args, **options):
        from apps.API_VK.VkBotClass import parse_msg
        from apps.API_VK.command.CommonMethods import remove_tz, localize_datetime

        notifies = Notify.objects.all()

        DATETIME_NOW = datetime.utcnow()
        # DATETIME_NOW = datetime(2020, 4, 18, 12, 30, 1)
        print(f'DATETIME_NOW: {DATETIME_NOW}\n')
        for notify in notifies:
            if notify.repeat:
                datetime1 = datetime.combine(date.min, remove_tz(notify.date).time())
                datetime2 = datetime.combine(date.min, DATETIME_NOW.time())
                delta_time = datetime1 - datetime2 + timedelta(minutes=1)
                flag = delta_time.seconds <= 60
                print(f"notify: {notify.text} - {notify.date}")
                print(f"datetime1: {datetime1}\ndatetime2: {datetime2}\ndelta_time:{delta_time}\nflag:{flag}\n")
            else:
                delta_time = remove_tz(notify.date) - DATETIME_NOW + timedelta(minutes=1)
                flag = delta_time.days == 0 and delta_time.seconds <= 60

            if flag:
                notify_datetime = localize_datetime(remove_tz(notify.date), notify.author.city.timezone)
                message = f"Напоминалка на {notify_datetime.strftime('%H:%M')}\n" \
                          f"[id{notify.author.user_id}|{notify.author}]:\n" \
                          f"{notify.text}"
                if notify.chat:
                    vk_bot.send_message(notify.chat.chat_id, message)
                else:
                    vk_bot.send_message(notify.author.user_id, message)

                # Если отложенная команда
                if notify.text.startswith('/'):
                    msg = notify.text[1:]
                    vk_event = {
                        'parsed': parse_msg(msg),
                        'sender': notify.author,
                    }
                    if notify.chat:
                        vk_event['chat'] = notify.chat
                        vk_event['peer_id'] = notify.chat.chat_id
                    else:
                        vk_event['chat'] = None
                        vk_event['peer_id'] = notify.author.user_id

                    vk_event_object = VkEvent(vk_event)
                    vk_bot.menu(vk_event_object, send=True)

                if notify.repeat:
                    # Для постоянных уведомлений дата должа быть на завтрашний день обязательно. Это важно для сортировки
                    new_datetime = datetime.combine(DATETIME_NOW.date(), notify.date.time()) + timedelta(days=1)
                    new_datetime = localize_datetime(remove_tz(new_datetime), notify.author.city.timezone)
                    notify.date = new_datetime
                    notify.save()
                else:
                    notify.delete()
        print(
            '----------------------------------------------------------------------------------------------------------------------------------------------------------')
