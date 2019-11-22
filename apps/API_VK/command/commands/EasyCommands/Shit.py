from apps.API_VK.command.CommonCommand import CommonCommand


class Shit(CommonCommand):
    def __init__(self):
        names = ["дерьмо"]
        super().__init__(names)

    def start(self):
        self.vk_bot.send_message(self.vk_event.chat_id, 'Ня')
