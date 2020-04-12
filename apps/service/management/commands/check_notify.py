from datetime import datetime, timedelta

from django.core.management.base import BaseCommand

from apps.API_VK.VkBotClass import parse_msg
from apps.API_VK.VkEvent import VkEvent
from apps.service.models import Notify
from xoma163site.wsgi import vk_bot


class Command(BaseCommand):

    def handle(self, *args, **options):
        from apps.API_VK.command.CommonMethods import remove_tz, localize_datetime

        notifies = Notify.objects.all()

        for notify in notifies:
            delta_time = remove_tz(notify.date) - datetime.utcnow() + timedelta(minutes=1)
            if delta_time.days == 0 and delta_time.seconds <= 60:

                notify_datetime = localize_datetime(remove_tz(notify.date), notify.author.city.timezone)
                message = f"Напоминалка на {notify_datetime.strftime('%H:%M')}\n" \
                          f"[id{notify.author.user_id}|{notify.author}]:\n" \
                          f"{notify.text}"
                if notify.from_chat:
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
                    if notify.from_chat:
                        vk_event['chat'] = notify.chat
                        vk_event['peer_id'] = notify.chat.chat_id
                    else:
                        vk_event['chat'] = None
                        vk_event['peer_id'] = notify.author.user_id

                    vk_event_object = VkEvent(vk_event)
                    vk_bot.menu(vk_event_object, send=True)

                if notify.repeat:
                    notify.date = notify.date + timedelta(days=1)
                    notify.save()
                else:
                    notify.delete()
