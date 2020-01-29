from apps.API_VK.command.CommonCommand import CommonCommand


class Donate(CommonCommand):
    def __init__(self):
        names = ["донат", "донаты"]
        help_text = "Донат - ссылка на донат"
        super().__init__(names, help_text)

    def start(self):
        return 'https://www.donationalerts.com/r/xoma163'
