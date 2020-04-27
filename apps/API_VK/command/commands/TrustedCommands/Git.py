from apps.API_VK.command.CommonCommand import CommonCommand


class Git(CommonCommand):
    def __init__(self):
        names = ["гит", "гитхаб"]
        help_text = "Гит - ссылка на гитхаб"
        super().__init__(names, help_text, access='trusted')

    def start(self):
        return 'https://github.com/Xoma163/xoma163site/'
