from datetime import datetime, timedelta

from django.core.management.base import BaseCommand

from apps.service.models import Notify
from xoma163site.wsgi import vk_bot


class Command(BaseCommand):

    def handle(self, *args, **options):
        from apps.API_VK.command.CommonMethods import remove_tz, localize_datetime

        notifies = Notify.objects.all()

        for notify in notifies:
            if (remove_tz(notify.date) - datetime.utcnow() + timedelta(minutes=1)).seconds <= 60:

                notify_datetime = localize_datetime(remove_tz(notify.date), notify.author.city.timezone)
                message = f"Напоминалка на {notify_datetime.strftime('%H:%M')}\n" \
                          f"[id{notify.author.user_id}|{notify.author}]:\n" \
                          f"{notify.text}"
                if notify.from_chat:
                    vk_bot.send_message(notify.chat.chat_id, message)
                else:
                    vk_bot.send_message(notify.author.user_id, message)
                notify.delete()
