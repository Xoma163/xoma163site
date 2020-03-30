from datetime import datetime

from django.core.management.base import BaseCommand

from apps.API_VK.models import VkChat, VkUser
from apps.games.models import Gamer
from xoma163site.wsgi import vk_bot


class Command(BaseCommand):

    def handle(self, *args, **options):
        from apps.API_VK.command.CommonMethods import get_mention

        chat_ids = options['chat_id'][0].split(',')
        for chat_id in chat_ids:
            chat = VkChat.objects.filter(chat_id=vk_bot.get_group_id(chat_id)).first()

            if not chat:
                print(f"Чата с id = {chat_id} не существует")
                break

            today = datetime.now()
            users = VkUser.objects.filter(chats=chat,
                                          birthday__day=today.day,
                                          birthday__month=today.month)

            for user in users:
                vk_bot.send_message(chat.chat_id, f"С Днём рождения, {get_mention(user)}!")

                gamer = Gamer.objects.filter(user=user).first()
                if gamer:
                    gamer.roulette_points += 10000
                    gamer.save()
                    vk_bot.send_message(chat.chat_id, f"Начислил 10 000 очков рулетки")

    def add_arguments(self, parser):
        parser.add_argument('chat_id', nargs='+', type=str,
                            help='chat_id')
