from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import random_probability


class Clear(CommonCommand):
    def __init__(self):
        names = ["ясно", "ммм"]
        super().__init__(names)

    def start(self):
        if self.vk_event.command == 'ммм':
            if random_probability(50):
                return "Данон"
        return "Хуета"
