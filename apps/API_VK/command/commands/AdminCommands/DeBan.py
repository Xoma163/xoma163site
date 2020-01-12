from apps.API_VK.command.CommonCommand import CommonCommand


class DeBan(CommonCommand):
    def __init__(self):
        names = ["разбан"]
        help_text = "̲Р̲а̲з̲б̲а̲н N - разбан пользователя"
        super().__init__(names, help_text, access='admin', need_args=1)

    def start(self):
        try:
            user = self.vk_bot.get_user_by_name(self.vk_event.args)
        except RuntimeError as e:
            return str(e)
        user.is_banned = False
        user.save()
        return "Разбанен"
