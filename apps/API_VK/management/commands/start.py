#!/var/www/xoma163.site/venv/bin/python -u

import os

from django.core.management import BaseCommand

from xoma163site.settings import BASE_DIR
from xoma163site.wsgi import cameraHandler, vk_bot


class Command(BaseCommand):

    def __init__(self):
        super().__init__()

    def handle(self, *args, **kwargs):
        if not os.path.exists(BASE_DIR + '/thread.lock'):
            open(BASE_DIR + '/thread.lock', 'w')
            vk_bot.start()
            cameraHandler.start()
            print("BOT AND CAMERA HANDLER STARTED")
