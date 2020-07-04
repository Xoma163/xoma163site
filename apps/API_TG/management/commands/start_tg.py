from django.core.management import BaseCommand

from apps.API_TG.TgBotClass import TgBotClass


class Command(BaseCommand):

    def __init__(self):
        super().__init__()

    def handle(self, *args, **kwargs):
        tg_bot = TgBotClass()
        tg_bot.start()
        print("TG BOT STARTED")
