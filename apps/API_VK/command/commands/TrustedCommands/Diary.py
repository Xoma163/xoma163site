from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.Consts import Role


class Diary(CommonCommand):
    def __init__(self):
        names = ["ежедневник"]
        help_text = "Ежедневник - ссылка на ежедневник"
        super().__init__(names, help_text, access=Role.TRUSTED)

    def start(self):
        url = 'https://diary.xoma163.xyz/'
        return {'msg': url, 'attachments': url}
