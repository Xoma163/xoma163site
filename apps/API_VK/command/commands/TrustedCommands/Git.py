from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.Consts import Role


class Git(CommonCommand):
    def __init__(self):
        names = ["гит", "гитхаб"]
        help_text = "Гит - ссылка на гитхаб"
        super().__init__(names, help_text, access=Role.TRUSTED)

    def start(self):
        url = 'https://github.com/Xoma163/xoma163site/'
        return {'msg': url, 'attachments': url}
