from apps.API_VK.command.CommonCommand import CommonCommand


class Ban(CommonCommand):
    def __init__(self):
        names = ["бан"]
        super().__init__(names, for_admin=True, check_args=True)

    def start(self):
        try:
            user = self.vk_bot.get_user_by_name(self.vk_event.args)
        except RuntimeError as e:
            self.vk_bot.send_message(self.vk_event.chat_id, str(e))
            return

        if user.is_admin:
            self.vk_bot.send_message(self.vk_event.chat_id, "Нельзя банить админа")
            return
        user.is_banned = True
        user.save()

        self.vk_bot.send_message(self.vk_event.chat_id, "Забанен")
