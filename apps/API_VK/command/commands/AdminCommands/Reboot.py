from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command._DoTheLinuxComand import do_the_linux_command


class Reboot(CommonCommand):
    def __init__(self):
        names = ["ребут"]
        help_text = "̲Р̲е̲б̲у̲т - перезагружает сервер."
        super().__init__(names, help_text, for_admin=True)

    def start(self):
        do_the_linux_command('sudo systemctl reboot -i')
