from django.contrib.auth.models import Group

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import check_user_group
from apps.API_VK.command.Consts import Role


class Ban(CommonCommand):
    def __init__(self):
        names = ["бан"]
        help_text = "Бан - бан пользователя"
        detail_help_text = "Бан (N) - бан пользователя, где N - имя, фамилия, логин/id, никнейм"
        super().__init__(names, help_text, detail_help_text, access=Role.ADMIN, args=1)

    def start(self):
        user = self.vk_bot.get_user_by_name(self.vk_event.args, self.vk_event.chat)

        if check_user_group(user, Role.ADMIN):
            return "Нельзя банить админа"
        group_banned = Group.objects.get(name=Role.BANNED.name)
        user.groups.add(group_banned)
        user.save()

        return "Забанен"
