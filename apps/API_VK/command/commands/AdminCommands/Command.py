from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.DoTheLinuxComand import do_the_linux_command


class Command(CommonCommand):
    def __init__(self):
        names = ["команда"]
        help_text = "Команда - запускает любую команду на сервере"
        detail_help_text = "Команда (команда) - запускает любую команду на сервере с уровнем прав server"
        super().__init__(names, help_text, detail_help_text, access=['admin', 'trusted'], args=1)

    def start(self):
        return do_the_linux_command(self.vk_event.original_args)
