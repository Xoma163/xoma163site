from apps.API_VK.command.CommonCommand import CommonCommand


class Start_lada(CommonCommand):
    def __init__(self):
        names = ["завести", "заведи"]
        super().__init__(names)

    def start(self):
        if self.vk_event.args:
            who = self.vk_event.params_without_keys
            return ["уи ви ви ви ви ви ви ви", f'завёл {who}']
            
        return "уи ви ви ви ви ви ви ви"
