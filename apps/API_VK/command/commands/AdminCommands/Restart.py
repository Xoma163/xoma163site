from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.Consts import Role
from apps.API_VK.command.DoTheLinuxComand import do_the_linux_command


class Restart(CommonCommand):
    def __init__(self):
        names = ["рестарт", "restart", "ребут"]
        help_text = "Рестарт - перезагружает бота или веб на сервере, либо сам сервер"
        detail_help_text = "Рестарт [сервис=бот] - перезагружает сервис\n" \
                           "Сервис - бот/веб/сервер"
        super().__init__(names, help_text, detail_help_text, access=Role.ADMIN.name)

    def start(self):
        module = "bot"
        if self.vk_event.args:
            module = self.vk_event.args[0]
        if module in ['бот', 'bot']:
            do_the_linux_command('sudo systemctl restart xoma163bot')
            return 'Рестартим бота'
        elif module in ['веб', 'web', 'сайт', 'site']:
            do_the_linux_command('sudo systemctl restart xoma163site')
            return 'Рестартим веб'
        elif module in ['сервер', 'server']:
            do_the_linux_command('sudo systemctl reboot -i')
            return 'Рестартим веб'
        else:
            return "Не найден такой модуль"
