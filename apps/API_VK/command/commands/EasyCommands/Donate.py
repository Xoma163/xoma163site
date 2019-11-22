from apps.API_VK.command.CommonCommand import CommonCommand


class Donate(CommonCommand):
    def __init__(self):
        names = ["донат", "донаты"]
        super().__init__(names)

    def start(self):
        self.vk_bot.send_message(self.vk_event.chat_id, 'https://www.donationalerts.com/r/xoma163')
