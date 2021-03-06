from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.Consts import Role
from apps.service.management.commands.get_words import Command


class Words(CommonCommand):
    def __init__(self):
        names = ["слова"]
        help_text = "Слова - принудительно затягивает слова с Google Drive"
        super().__init__(names, help_text, access=Role.MODERATOR)

    def start(self):
        get_words = Command()
        return get_words.handle()
