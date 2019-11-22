from apps.API_VK.command.CommonCommand import CommonCommand


class Thanks(CommonCommand):
    def __init__(self):
        names = ["спасибо", "спасибо!", "спс"]
        super().__init__(names)

    def start(self):
        msg = "Всегда пожалуйста :)"
        self.vk_bot.send_message(self.vk_event.chat_id, msg)
