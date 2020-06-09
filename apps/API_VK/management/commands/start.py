from django.core.management import BaseCommand

from apps.API_VK.VkBotClass import VkBotClass
from apps.birds.CameraHandler import CameraHandler

cameraHandler = CameraHandler()
vk_bot = VkBotClass()


class Command(BaseCommand):

    def __init__(self):
        super().__init__()

    def handle(self, *args, **kwargs):
        debug = kwargs['debug']
        if debug:
            vk_bot.DEVELOP_DEBUG = True
            vk_bot.start()
            print("BOT STARTED")
        else:
            vk_bot.start()
            cameraHandler.start()
            print("BOT AND CAMERA HANDLER STARTED")

    def add_arguments(self, parser):
        parser.add_argument('debug', type=bool, nargs='?', help='debug', default=False)
