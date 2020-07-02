from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.Consts import Role
from apps.API_VK.command.DoTheLinuxComand import do_the_linux_command


class Restart(CommonCommand):
    def __init__(self):
        names = ["рестарт", "ребут"]
        help_text = "Рестарт - перезагружает бота или веб на сервере, либо сам сервер"
        detail_help_text = "Рестарт [сервис=бот] - перезагружает сервис\n" \
                           "Сервис - бот/веб/сервер"
        super().__init__(names, help_text, detail_help_text, access=Role.ADMIN)

    def start(self):
        if self.vk_event.args:
            arg0 = self.vk_event.args[0].lower()
        else:
            arg0 = None
        menu = [
            [['бот'], self.menu_bot],
            [['веб', 'сайт'], self.menu_web],
            [['сервер'], self.menu_server],
            [['default'], self.menu_bot]
        ]
        method = self.handle_menu(menu, arg0)
        return method()

    def menu_bot(self):
        self.vk_bot.parse_and_send_msgs_thread(self.vk_event.peer_id, 'Рестартим бота')
        do_the_linux_command('sudo systemctl restart xoma163bot')
        return 'Рестартим бота'

    @staticmethod
    def menu_web():
        do_the_linux_command('sudo systemctl restart xoma163site')
        return 'Рестартим веб'

    @staticmethod
    def menu_server():
        do_the_linux_command('sudo systemctl reboot -i')
        return 'Рестартим сервер'
