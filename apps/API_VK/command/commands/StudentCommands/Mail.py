from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.static_texts import get_teachers_email


class Mail(CommonCommand):
    def __init__(self):
        names = ["почта"]
        super().__init__(names, for_student=True)

    def start(self):
        self.vk_bot.send_message(self.vk_event.chat_id, get_teachers_email())
