from apps.API_VK.command.CommonCommand import CommonCommand


class Sho(CommonCommand):
    def __init__(self):
        names = ["шо", "шоты", "тышо"]
        super().__init__(names)

    def start(self):
        return "я нишо а ты шо"
