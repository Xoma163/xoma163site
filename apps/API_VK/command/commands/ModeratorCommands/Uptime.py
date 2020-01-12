from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command._DoTheLinuxComand import do_the_linux_command


class Uptime(CommonCommand):
    def __init__(self):
        names = ["аптайм", "uptime"]
        help_text = "̲А̲п̲т̲а̲й̲м - аптайм сервера"
        super().__init__(names, help_text, access='moderator')

    def start(self):
        command = "uptime"
        result = do_the_linux_command(command)
        return result
