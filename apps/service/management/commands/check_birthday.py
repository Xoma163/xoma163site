from datetime import datetime

from django.core.management.base import BaseCommand

from apps.API_VK.models import VkChat, VkUser
from xoma163site.wsgi import vk_bot


class Command(BaseCommand):

    def handle(self, *args, **options):
        chat_ids = options['chat_id'][0].split(',')
        for chat_id in chat_ids:
            chat = VkChat.objects.filter(chat_id=vk_bot.get_group_id(chat_id))

            if not chat:
                print(f"Чата с id = {chat_id} не существует")
                break
            chat = chat.first()

            today = datetime.now()
            users = VkUser.objects.filter(chats__in=chat,
                                          birthday__day=today.day,
                                          birthday__month=today.month)

            for user in users:
                vk_bot.send_message(chat.chat_id, f"С Днём рождения, {user.name}!")

    def add_arguments(self, parser):
        parser.add_argument('chat_id', nargs='+', type=str,
                            help='chat_id')
