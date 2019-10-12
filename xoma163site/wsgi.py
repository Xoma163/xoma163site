"""
WSGI config for xoma163site project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

import django
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xoma163site.settings')

# ToDo: Ёбаный костыль, испанский стыд, просто пиздец. Переделай это когда будет время. Инициализация static переменной
django.setup()

from apps.birds.CameraHandler import CameraHandler
cameraHandler = CameraHandler(100)

from apps.API_VK.vkbot import VkBot
vkbot = VkBot()
if not os.path.exists('thread.lock'):
    cameraHandler.start()
    vkbot.start()
    print("BOT and CAMERA HANDLER STARTED")
else:
    print("BOT and CAMERA HANDLER  WILL BE NOT STARTED")

application = get_wsgi_application()
