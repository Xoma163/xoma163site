from django.core.management.base import BaseCommand
from django.db.models import Count

from apps.API_VK.VkEvent import VkEvent
from apps.games.models import Rate
from xoma163site.wsgi import vk_bot


class Command(BaseCommand):

    def handle(self, *args, **options):
        from apps.API_VK.command.commands.Games.Rates import Rates
        from apps.API_VK.models import VkChat

        rates_chats = Rate.objects.all().values('chat').annotate(count=Count('chat')).order_by()

        command = Rates()
        for rates in rates_chats:
            command.vk_event = VkEvent(
                {'chat': VkChat.objects.get(id=rates['chat']),
                 'command': 'ставки'})
            command.vk_event.args = []
            command.vk_bot = vk_bot
            result = command.start()
            # Небольшой костыльчик, ну типа только если идёт розыгрыш, тогда возвращается list
            if isinstance(result, list):
                vk_bot.parse_and_send_msgs(command.vk_event.chat.chat_id, result)
