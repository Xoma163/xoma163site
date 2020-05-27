from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.Consts import Role
from apps.API_VK.command.DoTheLinuxComand import do_the_linux_command


class Linux(CommonCommand):
    def __init__(self):
        names = ["линукс", "linux", "консоль", "терминал"]
        help_text = "Линукс - запускает любую команду на сервере"
        detail_help_text = "Линукс (команда) - запускает любую команду на сервере с уровнем прав server"
        super().__init__(names, help_text, detail_help_text, access=Role.ADMIN.name, args=1)

    def start(self):
        return do_the_linux_command(self.vk_event.original_args)
