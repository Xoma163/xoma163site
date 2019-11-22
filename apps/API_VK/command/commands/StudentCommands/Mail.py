from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.static_texts import get_teachers_email


class Mail(CommonCommand):
    def __init__(self):
        names = ["почта"]
        help_text = "̲П̲о̲ч̲т̲а - почты преподов"
        super().__init__(names, help_text, for_student=True)

    def start(self):
        self.vk_bot.send_message(self.vk_event.chat_id, get_teachers_email())
