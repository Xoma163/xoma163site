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

django.setup()

from apps.birds.CameraHandler import CameraHandler

cameraHandler = CameraHandler()
from apps.API_VK.VkBot import VkBot

vk_bot = VkBot()
# if not os.path.exists(BASE_DIR + '/thread.lock'):
#     open(BASE_DIR + '/thread.lock', 'w')
#
#     cameraHandler.start()
#     vk_bot.start()
#     print("BOT AND CAMERA HANDLER STARTED")
# else:
#     print("BOT and CAMERA HANDLER  WILL BE NOT STARTED")
application = get_wsgi_application()
