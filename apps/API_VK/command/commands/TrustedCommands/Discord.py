from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.Consts import Role


class Discord(CommonCommand):
    def __init__(self):
        names = ["дискорд", "диск"]
        help_text = "Дискорд - ссылка на канал в дискорде"
        super().__init__(names, help_text, access=Role.TRUSTED)

    def start(self):
        url = 'https://discord.gg/kYGSNzv'
        return {'msg': url, 'attachments': url}
