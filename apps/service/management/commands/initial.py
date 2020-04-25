from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    @staticmethod
    def init_groups():
        from apps.API_VK.command.CommonCommand import role_translator
        groups = [{'name': x} for x in role_translator]
        for group in groups:
            Group.objects.update_or_create(name=group['name'], defaults=group)

    @staticmethod
    def init_cities():
        pass

    def handle(self, *args, **options):
        self.init_groups()
        print('done init groups')

        self.init_cities()
        print('done init cities')

        print("done all")
