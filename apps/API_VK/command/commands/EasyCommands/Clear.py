from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import random_event


class Clear(CommonCommand):
    def __init__(self):
        names = ["ясно", "ммм"]
        super().__init__(names)

    def start(self):
        if self.vk_event.command == 'ммм':
            return random_event(["Данон", "Хуета"], [50, 50])
