from apps.API_VK.command.CommonCommand import CommonCommand, check_sender_admin, check_sender_minecraft, \
    check_command_time
from apps.API_VK.command._DoTheLinuxComand import do_the_linux_command
from xoma163site.wsgi import cameraHandler


class Stop(CommonCommand):
    def __init__(self):
        names = ["стоп"]
        help_text = "̲С̲т̲о̲п - останавливает работу Петровича. " \
                    "С параметром можно отключить нужный модуль (синички, майн(1.12 1.15))"
        super().__init__(names, help_text, for_moderator=True)

    def start(self):
        if self.vk_event.args:
            if self.vk_event.args[0] == "синички":
                if cameraHandler.is_active():
                    cameraHandler.terminate()
                    self.vk_bot.send_message(self.vk_event.chat_id, "Финишируем синичек")
                else:
                    self.vk_bot.send_message(self.vk_event.chat_id, "Синички уже финишировали")
            elif self.vk_event.args[0] in ["майн", "майнкрафт"]:
                if not check_sender_minecraft(self.vk_bot, self.vk_event):
                    return
                if len(self.vk_event.args) >= 2:
                    if self.vk_event.args[1] == '1.12':
                        if not check_command_time(self.vk_bot, self.vk_event, 'minecraft 1.12', 90):
                            return

                        do_the_linux_command('sudo systemctl stop minecraft')
                        self.vk_bot.send_message(self.vk_event.chat_id, "Финишируем майн 1.12!")
                    elif self.vk_event.args[1] == '1.15':
                        if not check_command_time(self.vk_bot, self.vk_event, 'minecraft 1.15', 30):
                            return

                        do_the_linux_command('sudo systemctl stop minecraft_1_15')
                        self.vk_bot.send_message(self.vk_event.chat_id, "Финишируем майн 1.15!")
                    else:
                        self.vk_bot.send_message(self.vk_event.chat_id,
                                                 "Я знаю такой версии {}".format(self.vk_event.args[1]))
                else:
                    self.vk_bot.send_message(self.vk_event.chat_id, "Не указана версия")
            else:
                self.vk_bot.send_message(self.vk_event.chat_id, "Не найден такой модуль")
        else:
            if not check_sender_admin(self.vk_bot, self.vk_event):
                return
            self.vk_bot.BOT_CAN_WORK = False
            cameraHandler.terminate()
            self.vk_bot.send_message(self.vk_event.chat_id, "Финишируем")
