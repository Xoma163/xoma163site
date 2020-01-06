from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command._DoTheLinuxComand import do_the_linux_command
from xoma163site.wsgi import cameraHandler


class Start(CommonCommand):
    def __init__(self):
        names = ["старт", "start"]
        help_text = "̲С̲т̲а̲р̲т - возобновляет работу Петровича(только для админов). " \
                    "С параметром можно включить нужный модуль (синички, майн(1.12 1.15.1))"
        keyboard_admin = [{'text': 'Старт', 'color': 'green', 'row': 1, 'col': 1},
                          {'text': 'Старт синички', 'color': 'green', 'row': 1, 'col': 3}]
        super().__init__(names, help_text, keyboard_admin=keyboard_admin)

    def start(self):
        if self.vk_event.args:

            if self.vk_event.args[0] == "синички":
                if not self.check_sender_moderator():
                    return
                if not cameraHandler.is_active():
                    cameraHandler.resume()
                    return "Стартуем синичек!"
                else:
                    return "Синички уже стартовали"
            elif self.vk_event.args[0] in ["майн", "майнкрафт", "mine", "minecraft"]:
                if not self.check_sender_minecraft():
                    return
                if len(self.vk_event.args) >= 2:
                    if self.vk_event.args[1] == '1.12':
                        if not self.check_command_time('minecraft 1.12', 90):
                            return

                        do_the_linux_command('sudo systemctl start minecraft')
                        return "Стартуем майн 1.12!"
                    elif self.vk_event.args[1] == '1.15.1':
                        if not self.check_command_time('minecraft 1.15.1', 30):
                            return

                        do_the_linux_command('sudo systemctl start minecraft_1_15_1')
                        return "Стартуем майн 1.15.1!"
                    else:
                        return "Я знаю такой версии {}".format(self.vk_event.args[1])
                else:
                    return "Не указана версия"
            elif self.vk_event.args[0] in ['террария', 'terraria']:
                if not self.check_sender_terraria():
                    return
                if not self.check_command_time('terraria', 10):
                    return
                do_the_linux_command('sudo systemctl start terraria')
                return "Стартуем террарию!"
            else:
                return "Не найден такой модуль"
        else:
            if not self.check_sender_admin():
                return

            self.vk_bot.BOT_CAN_WORK = True
            return "Стартуем!"
