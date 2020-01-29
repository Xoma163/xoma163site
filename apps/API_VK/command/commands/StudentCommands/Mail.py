from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.static_texts import get_teachers_email


class Mail(CommonCommand):
    def __init__(self):
        names = ["почта"]
        help_text = "Почта - почты преподов"
        keyboard = {'for': 'student', 'text': 'Почта', 'color': 'blue', 'row': 1, 'col': 4}
        super().__init__(names, help_text, access='student', keyboard=keyboard)

    def start(self):
        return get_teachers_email()
