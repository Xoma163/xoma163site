from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import get_user_groups


class Keyboard(CommonCommand):
    def __init__(self):
        names = ["клава", "клавиатура"]
        help_text = "Клава - показать клавиатуру"
        super().__init__(names, help_text, api=False)

    def start(self):
        return {"keyboard": get_keyboard(self.vk_event.sender)}


def get_keyboard(sender):
    from apps.API_VK.command import KEYBOARDS

    buttons = []

    user_groups = get_user_groups(sender)

    for group in user_groups:
        buttons += KEYBOARDS[group]

    keyboard = {
        "one_time": False,
        "buttons": buttons
    }
    return keyboard
