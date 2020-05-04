from apps.API_VK.command.CommonCommand import CommonCommand


class GameConference(CommonCommand):
    def __init__(self):
        names = ["игровая", "ставошная"]
        help_text = "Игровая - ссылка-приглашение в игровую конфу"
        super().__init__(names, help_text)

    def start(self):
        # return 'https://vk.me/join/AJQ1d0fAnhYSoISi2sowQoe3'
        return 'https://vk.me/join/AJQ1d9ppmRflxVoEplfcaUHv'
