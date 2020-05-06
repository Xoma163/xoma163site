import datetime

from apps.API_VK.command import Role
from apps.API_VK.command.CommonCommand import CommonCommand


class Week(CommonCommand):
    def __init__(self):
        names = ["неделя"]
        help_text = "Неделя - номер текущей учебной недели"
        keyboard_student = {'text': 'Неделя', 'color': 'blue', 'row': 1, 'col': 1}
        super().__init__(names, help_text, access=Role.TERRARIA.name, keyboard=keyboard_student, enabled=False)

    def start(self):
        return str((datetime.datetime.now().isocalendar()[1] - 35)) + " неделя"
