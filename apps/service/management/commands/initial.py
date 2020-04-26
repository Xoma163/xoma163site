from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from apps.API_VK.models import VkUser, APIUser


class Command(BaseCommand):

    @staticmethod
    def init_groups():
        from apps.API_VK.command.CommonCommand import role_translator
        groups = [{'name': x} for x in role_translator]
        for group in groups:
            Group.objects.update_or_create(name=group['name'], defaults=group)

    @staticmethod
    def init_users():
        anonymous_user = {
            'user_id': 'ANONYMOUS',
            'name': 'Аноним',
            'surname': 'Анонимов'
        }
        anon_user, _ = VkUser.objects.update_or_create(user_id=anonymous_user['user_id'], defaults=anonymous_user)
        group_user = Group.objects.get(name='user')
        anon_user.groups.add(group_user)
        anon_user.save()

        api_anonymous_user = {
            'user_id': 'ANONYMOUS',
            'vk_user': anon_user,
            'vk_chat': None
        }
        APIUser.objects.update_or_create(user_id=api_anonymous_user['user_id'], defaults=api_anonymous_user)

    @staticmethod
    def init_cities():
        pass

    def handle(self, *args, **options):
        self.init_groups()
        print('done init groups')

        self.init_users()
        print('done init users')

        self.init_cities()
        print('done init cities')

        print("done all")
