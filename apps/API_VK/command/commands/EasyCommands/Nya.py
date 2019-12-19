from apps.API_VK.command.CommonCommand import CommonCommand


class Nya(CommonCommand):
    def __init__(self):
        names = ["ня"]
        super().__init__(names)

    def start(self):
        return "Дерьмо"
