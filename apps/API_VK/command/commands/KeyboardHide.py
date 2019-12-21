import json

from apps.API_VK.command.CommonCommand import CommonCommand


class KeyboardHide(CommonCommand):
    def __init__(self):
        names = ["убери", "скрыть"]
        help_text = "̲С̲к̲р̲ы̲т̲ь - убирает клавиатуру"
        keyboard_user = {'text': 'Скрыть', 'color': 'gray', 'row': 3, 'col': 1}

        super().__init__(names, help_text, keyboard_user=keyboard_user)

    def start(self):
        keyboard = {
            "one_time": False,
            "buttons": []
        }
        return {'msg': 'Убрал', 'keyboard': json.dumps(keyboard)}
