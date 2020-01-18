from apps.API_VK.command.CommonCommand import CommonCommand


class Start_lada(CommonCommand):
    def __init__(self):
        names = ["завести", "заведи"]
        super().__init__(names)

    def start(self):
        return "уи ви ви ви ви ви ви ви"
