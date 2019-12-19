from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command._DoTheLinuxComand import do_the_linux_command


class Words(CommonCommand):
    def __init__(self):
        names = ["слова", "get_words"]
        help_text = "̲С̲л̲о̲в̲а - принудительно затягивает слова с Google Drive"
        super().__init__(names, help_text, for_moderator=True)

    def start(self):
        command = "/var/www/xoma163.site/venv/bin/python /var/www/xoma163.site/manage.py get_words"
        result = do_the_linux_command(command)
        if not result:
            result = "done"
        return result
