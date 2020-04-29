from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.DoTheLinuxComand import do_the_linux_command


class Uptime(CommonCommand):
    def __init__(self):
        names = ["аптайм", "uptime"]
        help_text = "Аптайм - аптайм сервера"
        super().__init__(names, help_text, access='moderator')

    def start(self):
        command = "uptime"
        result = do_the_linux_command(command)
        return result
