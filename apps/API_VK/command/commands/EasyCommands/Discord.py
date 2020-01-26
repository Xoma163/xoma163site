from apps.API_VK.command.CommonCommand import CommonCommand


class Discord(CommonCommand):
    def __init__(self):
        names = ["дискорд", "диск"]
        help_text = "̲Д̲и̲с̲к̲о̲р̲д - ссылка на канал в дискорде"
        super().__init__(names, help_text)

    def start(self):
        return "https://discord.gg/kYGSNzv"
