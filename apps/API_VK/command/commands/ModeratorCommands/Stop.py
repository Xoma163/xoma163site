from apps.API_VK.command.CommonCommand import CommonCommand, check_sender_admin
from apps.API_VK.command._DoTheLinuxComand import do_the_linux_command
from xoma163site.wsgi import cameraHandler


class Stop(CommonCommand):
    def __init__(self):
        names = ["стоп"]
        help_text = "̲С̲т̲о̲п - останавливает работу Петровича. " \
                    "С параметром можно отключить нужный модуль (синички, майн)"
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
                do_the_linux_command('sudo systemctl stop minecraft')
                self.vk_bot.send_message(self.vk_event.chat_id, "Финишируем майн")
            else:
                self.vk_bot.send_message(self.vk_event.chat_id, "Не найден такой модуль")
        else:
            if not check_sender_admin(self.vk_bot, self.vk_event):
                return
            self.vk_bot.BOT_CAN_WORK = False
            self.vk_bot.send_message(self.vk_event.chat_id, "Финишируем")
