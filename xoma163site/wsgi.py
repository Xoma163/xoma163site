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

from apps.API_VK.VkBotClass import VkBotClass

vk_bot = VkBotClass()
application = get_wsgi_application()
