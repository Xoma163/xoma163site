from apps.API_VK.command.CommonCommand import CommonCommand


class Git(CommonCommand):
    def __init__(self):
        names = ["гит", "гитхаб"]
        help_text = "̲Г̲и̲т - ссылка на гитхаб"
        super().__init__(names, help_text)

    def start(self):
        self.vk_bot.send_message(self.vk_event.chat_id, 'https://github.com/Xoma163/xoma163site/')
