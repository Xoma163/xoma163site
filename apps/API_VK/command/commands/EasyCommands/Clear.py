from apps.API_VK.command.CommonCommand import CommonCommand


class Clear(CommonCommand):
    def __init__(self):
        names = ["ясно", "ммм"]
        super().__init__(names)

    def start(self):
        return "Хуета"
