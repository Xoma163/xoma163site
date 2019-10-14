from django.core.management.base import BaseCommand

from xoma163site.wsgi import vkbot
from apps.API_VK.yandex_weather import get_weather


class Command(BaseCommand):

    def handle(self, *args, **options):
        chat_ids = options['chat_id'][0].split(',')
        city = options['city'][0].lower()
        weather = get_weather(city)

        for chat_id in chat_ids:
            vkbot.send_message(chat_id, weather)

    def add_arguments(self, parser):
        parser.add_argument('chat_id', nargs='+', type=str  ,
                            help='chat_id')
        parser.add_argument('city', nargs='+', type=str,
                            help='city')