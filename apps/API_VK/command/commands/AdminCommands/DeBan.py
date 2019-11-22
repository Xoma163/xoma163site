from apps.API_VK.command.CommonCommand import CommonCommand


class DeBan(CommonCommand):
    def __init__(self):
        names = ["разбан"]
        super().__init__(names, for_admin=True, check_args=True)

    def start(self):
        try:
            user = self.vk_bot.get_user_by_name(self.vk_event.args)
        except RuntimeError as e:
            self.vk_bot.send_message(self.vk_event.chat_id, str(e))
            return
        user.is_banned = False
        user.save()
        self.vk_bot.send_message(self.vk_event.chat_id, "Разбанен")
