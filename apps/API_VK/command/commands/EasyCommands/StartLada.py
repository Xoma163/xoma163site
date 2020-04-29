from apps.API_VK.command.CommonCommand import CommonCommand


class StartLada(CommonCommand):
    def __init__(self):
        names = ["завести", "заведи"]
        super().__init__(names)

    def start(self):
        if self.vk_event.args:
            who = self.vk_event.original_args
            return ["уи ви ви ви ви ви ви ви", f'завёл {who}']

        return "уи ви ви ви ви ви ви ви"
