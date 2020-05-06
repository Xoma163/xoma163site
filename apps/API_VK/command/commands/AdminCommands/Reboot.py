from apps.API_VK.command import Role
from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.DoTheLinuxComand import do_the_linux_command


class Reboot(CommonCommand):
    def __init__(self):
        names = ["ребут"]
        help_text = "Ребут - перезагружает сервер"
        detail_help_text = "Ребут - перезагружает весь сервер аппаратно. Поднимется ли обратно - полностью на твоей ответственности"
        super().__init__(names, help_text, detail_help_text, access=[Role.ADMIN.name, Role.TRUSTED.name])

    def start(self):
        do_the_linux_command('sudo systemctl reboot -i')
