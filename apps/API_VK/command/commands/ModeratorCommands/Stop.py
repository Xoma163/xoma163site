from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command._DoTheLinuxComand import do_the_linux_command
from xoma163site.wsgi import cameraHandler


class Stop(CommonCommand):
    def __init__(self):
        names = ["стоп"]
        help_text = "̲С̲т̲о̲п - останавливает работу Петровича. " \
                    "С параметром можно отключить нужный модуль (синички, майн(1.12 1.15))"
        keyboard_admin = [{'text': 'Стоп', 'color': 'red', 'row': 1, 'col': 2},
                          {'text': 'Стоп синички', 'color': 'red', 'row': 1, 'col': 4}]

        super().__init__(names, help_text, for_moderator=True, keyboard_admin=keyboard_admin)

    def start(self):
        if self.vk_event.args:
            if self.vk_event.args[0] == "синички":
                if cameraHandler.is_active():
                    cameraHandler.terminate()
                    return "Финишируем синичек"
                else:
                    return "Синички уже финишировали"
            elif self.vk_event.args[0] in ["майн", "майнкрафт"]:
                if not self.check_sender_minecraft():
                    return
                if len(self.vk_event.args) >= 2:
                    if self.vk_event.args[1] == '1.12':
                        if not self.check_command_time('minecraft 1.12', 90):
                            return

                        do_the_linux_command('sudo systemctl stop minecraft')
                        return "Финишируем майн 1.12!"
                    elif self.vk_event.args[1] == '1.15':
                        if not self.check_command_time('minecraft 1.15', 30):
                            return

                        do_the_linux_command('sudo systemctl stop minecraft_1_15')
                        return "Финишируем майн 1.15!"
                    else:
                        return "Я знаю такой версии {}".format(self.vk_event.args[1])
                else:
                    return "Не указана версия"
            else:
                return "Не найден такой модуль"
        else:
            if not self.check_sender_admin():
                return
            self.vk_bot.BOT_CAN_WORK = False
            cameraHandler.terminate()
            return "Финишируем"
