from apps.API_VK.command.CommonCommand import CommonCommand


class update_users(CommonCommand):
    def __init__(self):
        names = ["update_users"]
        super().__init__(names, for_admin=True)

    def start(self):
        self.vk_bot.update_users()
        self.vk_bot.send_message(self.vk_event.chat_id, "done")
