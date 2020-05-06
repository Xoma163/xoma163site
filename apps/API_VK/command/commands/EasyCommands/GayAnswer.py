from apps.API_VK.command.CommonCommand import CommonCommand


class GayAnswer(CommonCommand):
    def __init__(self):
        names = ["пидора"]
        super().__init__(names)

    def start(self):
        if self.vk_event.args and self.vk_event.args[0].lower() == "ответ":
            return "Шлюхи аргумент"
        return None
