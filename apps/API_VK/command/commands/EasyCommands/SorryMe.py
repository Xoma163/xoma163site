from apps.API_VK.command.CommonCommand import CommonCommand


class SorryMe(CommonCommand):
    def __init__(self):
        names = ['извиниться']
        super().__init__(names)

    def start(self):
        return f"{self.vk_event.sender} извиняется перед всеми"
