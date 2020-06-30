from django.core.management.base import BaseCommand

from apps.API_VK.APIs.Minecraft import servers_minecraft
from apps.API_VK.VkBotClass import VkBotClass

vk_bot = VkBotClass()


class Command(BaseCommand):

    def handle(self, *args, **options):
        for server in servers_minecraft:
            server.stop_if_need()
