from apps.API_VK.command.CommonCommand import CommonCommand


class Discord(CommonCommand):
    def __init__(self):
        names = ["дискорд", "диск"]
        super().__init__(names)

    def start(self):
        return "https://discord.gg/kYGSNzv"
