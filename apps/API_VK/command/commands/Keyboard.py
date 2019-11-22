import json

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.static_texts import get_keyboard


class Keyboard(CommonCommand):
    def __init__(self):
        names = ["клава", "клавиатура"]
        help_text = "̲К̲л̲а̲в̲а - показать клавиатуру"
        super().__init__(names, help_text)

    def start(self):
        self.vk_bot.send_message(self.vk_event.chat_id, 'Лови', keyboard=json.dumps(
            get_keyboard(self.vk_event.sender.is_admin, self.vk_event.sender.is_student)))
