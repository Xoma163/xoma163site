from django.core.management.base import BaseCommand

from xoma163site.wsgi import vkbot


class Command(BaseCommand):
    # help = 'Displays current time'

    # python manage.py check_rasp
    # ToDo: Намутить расписание группы в json
    def handle(self, *args, **kwargs):
        vkbot.vk.messages.editChat(chat_id=2, title='6221 | %s %s - %s' % ("11:20", "Лёзина", "421"))
