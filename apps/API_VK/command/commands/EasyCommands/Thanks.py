from apps.API_VK.command.CommonCommand import CommonCommand


class Thanks(CommonCommand):
    def __init__(self):
        names = ["спасибо", "спасибо!", "спс"]
        super().__init__(names)

    def start(self):
        return "Всегда пожалуйста :)"
