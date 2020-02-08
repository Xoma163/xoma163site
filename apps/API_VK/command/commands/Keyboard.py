from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import check_user_role


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

    if check_user_role(sender, 'admin'):
        buttons += KEYBOARDS['admin']
    if check_user_role(sender, 'moderator'):
        buttons += KEYBOARDS['moderator']
    if check_user_role(sender, 'student'):
        buttons += KEYBOARDS['student']
    if check_user_role(sender, 'minecraft'):
        buttons += KEYBOARDS['minecraft']
    buttons += KEYBOARDS['user']

    keyboard = {
        "one_time": False,
        "buttons": buttons
    }
    return keyboard
