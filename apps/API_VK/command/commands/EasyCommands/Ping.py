from apps.API_VK.command.CommonCommand import CommonCommand


class Ping(CommonCommand):
    def __init__(self):
        names = ["пинг"]
        super().__init__(names)

    def start(self):
        return "Понг"
