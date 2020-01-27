from apps.API_VK.command.CommonCommand import CommonCommand


class Ban(CommonCommand):
    def __init__(self):
        names = ["бан"]
        help_text = "̲Б̲а̲н - бан пользователя"
        detail_help_text = "Бан (N) - бан пользователя, где N - имя, фамилия, логин/id, никнейм"
        super().__init__(names, help_text, detail_help_text, access='admin', need_args=1)

    def start(self):
        try:
            user = self.vk_bot.get_user_by_name(self.vk_event.args)
        except RuntimeError as e:
            return str(e)

        if user.is_admin:
            return "Нельзя банить админа"
        user.is_banned = True
        user.save()

        return "Забанен"
