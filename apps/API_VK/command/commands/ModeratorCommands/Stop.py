from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command._DoTheLinuxComand import do_the_linux_command
from xoma163site.wsgi import cameraHandler


class Stop(CommonCommand):
    def __init__(self):
        names = ["стоп", "stop"]
        help_text = "̲С̲т̲о̲п - останавливает работу Петровича. " \
                    "С параметром можно отключить нужный модуль (синички, майн(1.12 1.15.1))"
        keyboard_admin = [{'text': 'Стоп', 'color': 'red', 'row': 1, 'col': 2},
                          {'text': 'Стоп синички', 'color': 'red', 'row': 1, 'col': 4}]

        super().__init__(names, help_text, keyboard_admin=keyboard_admin)

    def start(self):
        if self.vk_event.args:
            if self.vk_event.args[0] == "синички":
                if not self.check_sender_moderator():
                    return
                if cameraHandler.is_active():
                    cameraHandler.terminate()
                    return "Финишируем синичек"
                else:
                    return "Синички уже финишировали"
            elif self.vk_event.args[0] in ["майн", "майнкрафт", "mine", "minecraft"]:
                if not self.check_sender_minecraft():
                    return
                if len(self.vk_event.args) >= 2:
                    if self.vk_event.args[1] == '1.12':
                        if not self.check_command_time('minecraft 1.12', 90):
                            return

                        do_the_linux_command('sudo systemctl stop minecraft')
                        return "Финишируем майн 1.12!"
                    elif self.vk_event.args[1] == '1.15.1':
                        if not self.check_command_time('minecraft 1.15.1', 30):
                            return

                        do_the_linux_command('sudo systemctl stop minecraft_1_15_1')
                        return "Финишируем майн 1.15.1!"
                    else:
                        return "Я знаю такой версии {}".format(self.vk_event.args[1])
                else:
                    return "Не указана версия"
            elif self.vk_event.args[0] in ['террария', 'terraria']:
                if not self.check_sender_terraria():
                    return
                if not self.check_command_time('terraria', 10):
                    return
                do_the_linux_command('sudo systemctl stop terraria')
                return "Финишируем террарию!"
            else:
                return "Не найден такой модуль"
        else:
            if not self.check_sender_admin():
                return
            self.vk_bot.BOT_CAN_WORK = False
            cameraHandler.terminate()
            return "Финишируем"
