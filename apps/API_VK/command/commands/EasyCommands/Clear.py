from apps.API_VK.command.CommonCommand import CommonCommand


class Clear(CommonCommand):
    def __init__(self):
        names = ["ясно"]
        super().__init__(names)

    def start(self):
        self.vk_bot.send_message(self.vk_event.chat_id, 'хуета')
