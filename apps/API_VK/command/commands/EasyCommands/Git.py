from apps.API_VK.command.CommonCommand import CommonCommand


class Git(CommonCommand):
    def __init__(self):
        names = ["гит", "гитхаб"]
        super().__init__(names)

    def start(self):
        self.vk_bot.send_message(self.vk_event.chat_id, 'https://github.com/Xoma163/xoma163site/')
