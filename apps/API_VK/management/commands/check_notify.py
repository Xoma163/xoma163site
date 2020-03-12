from datetime import datetime, timedelta

from django.core.management.base import BaseCommand

from apps.service.models import Notify
from xoma163site.wsgi import vk_bot


class Command(BaseCommand):

    def handle(self, *args, **options):
        notifies = Notify.objects.all()

        for notify in notifies:
            print((notify.date - datetime.now()).seconds)
            if (notify.date - datetime.now() + timedelta(minutes=1)).seconds <= 60:
                message = f"Напоминалка на {notify.date.strftime('%H:%M')}\n" \
                          f"{notify.author}:\n" \
                          f"{notify.text}"
                if notify.from_chat:
                    vk_bot.send_message(notify.chat.chat_id, message)
                else:
                    vk_bot.send_message(notify.author.user_id, message)
                notify.delete()
