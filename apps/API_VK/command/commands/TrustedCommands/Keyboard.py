from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import get_user_groups
from apps.API_VK.command.Consts import Role


class Keyboard(CommonCommand):
    def __init__(self):
        names = ["клава", "клавиатура"]
        help_text = "Клава - показать клавиатуру"
        # ToDo: access trusted это временное решение. Нужно будет пересмотреть политику клавиатур
        super().__init__(names, help_text, api=False, access=Role.TRUSTED.name)

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
