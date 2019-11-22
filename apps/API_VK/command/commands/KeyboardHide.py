import json

from apps.API_VK.command.CommonCommand import CommonCommand


class KeyboardHide(CommonCommand):
    def __init__(self):
        names = ["убери", "скрыть"]
        help_text = "̲С̲к̲р̲ы̲т̲ь - убирает клавиатуру"
        super().__init__(names, help_text)

    def start(self):
        keyboard = {
            "one_time": False,
            "buttons": []
        }
        self.vk_bot.send_message(self.vk_event.chat_id, 'Убрал', keyboard=json.dumps(keyboard))
