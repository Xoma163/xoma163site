from django.contrib.auth.models import Group

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.Consts import Role


class DeBan(CommonCommand):
    def __init__(self):
        names = ["разбан", "дебан"]
        help_text = "Разбан - разбан пользователя"
        detail_help_text = "Разбан (N) - разбан пользователя, где N - имя, фамилия, логин/id, никнейм"
        super().__init__(names, help_text, detail_help_text, access=Role.ADMIN, args=1)

    def start(self):
        user = self.vk_bot.get_user_by_name(self.vk_event.args, self.vk_event.chat)
        group_banned = Group.objects.get(name=Role.BANNED.name)
        user.groups.remove(group_banned)
        user.save()
        return "Разбанен"
