from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.Consts import Role


class Discord(CommonCommand):
    def __init__(self):
        names = ["дискорд", "диск"]
        help_text = "Дискорд - ссылка на канал в дискорде"
        super().__init__(names, help_text, access=Role.TRUSTED.name)

    def start(self):
        return "https://discord.gg/kYGSNzv"
