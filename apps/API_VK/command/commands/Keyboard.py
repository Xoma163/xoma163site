from apps.API_VK.command.CommonCommand import CommonCommand


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

    if sender.is_admin:
        buttons += KEYBOARDS['admin']
    if sender.is_moderator:
        buttons += KEYBOARDS['moderator']
    if sender.is_student:
        buttons += KEYBOARDS['student']
    if sender.is_minecraft:
        buttons += KEYBOARDS['minecraft']
    buttons += KEYBOARDS['user']

    keyboard = {
        "one_time": False,
        "buttons": buttons
    }
    return keyboard
