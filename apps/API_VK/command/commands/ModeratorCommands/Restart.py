from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command._DoTheLinuxComand import do_the_linux_command


class Restart(CommonCommand):
    def __init__(self):
        names = ["рестарт", "restart"]
        help_text = "Рестарт - перезагружает бота или модуль"
        detail_help_text = "Рестарт [сервис=бот [версия=1.15.1]] - перезагружает сервис.\n" \
                           "Сервис - бот/майнкрафт/террарию/сайт.\n" \
                           "Если майнкрафт, то может быть указана версия, 1.12.2 или 1.15.1"
        super().__init__(names, help_text, detail_help_text)

    def start(self):
        if self.vk_event.args:
            if self.vk_event.args[0] in ["майн", "майнкрафт", "mine", "minecraft"]:
                self.check_sender('minecraft')
                if len(self.vk_event.args) >= 2 and self.vk_event.args[1] == '1.12':
                    self.check_command_time('minecraft 1.12', 90)

                    do_the_linux_command('sudo systemctl start minecraft')
                    return "Рестартим майн 1.12!"
                elif (len(self.vk_event.args) >= 2 and self.vk_event.args[1] == '1.15.1') or len(
                        self.vk_event.args) == 1:
                    self.check_command_time('minecraft 1.15.1', 30)

                    do_the_linux_command('sudo systemctl start minecraft_1_15_1')
                    return "Рестартим майн 1.15.1!"
                else:
                    return "Я не знаю такой версии"
            elif self.vk_event.args[0] in ['террария', 'terraria']:
                self.check_sender('terraria')
                self.check_command_time('terraria', 10)

                do_the_linux_command('sudo systemctl start terraria')
                return "Рестартим террарию!"
            elif self.vk_event.args[0] in ['бот', 'bot']:
                self.check_sender('admin')
                do_the_linux_command('sudo systemctl restart xoma163bot')
                return 'Рестартим бота'
            elif self.vk_event.args[0] in ['веб', 'web', 'сайт', 'site']:
                self.check_sender('admin')
                do_the_linux_command('sudo systemctl restart xoma163site')
                return 'Рестартим веб'
            else:
                return "Не найден такой модуль"
        else:
            self.check_sender('admin')
            do_the_linux_command('sudo systemctl restart xoma163bot')
            return 'Рестартим бота'
