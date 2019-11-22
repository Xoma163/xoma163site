from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.static_texts import get_help_text


class Help(CommonCommand):
    def __init__(self):
        names = ["помощь", "хелп", "ман", "команды", "помоги", "памаги", "спаси", "хелб", "манул", "help"]
        super().__init__(names)

    def start(self):
        self.vk_bot.send_message(self.vk_event.chat_id,
                                 get_help_text(self.vk_event.sender.is_admin, self.vk_event.sender.is_student))
