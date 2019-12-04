from apps.API_VK.command.CommonCommand import CommonCommand, check_sender_admin
from apps.API_VK.command._DoTheLinuxComand import do_the_linux_command
from xoma163site.wsgi import cameraHandler


class Start(CommonCommand):
    def __init__(self):
        names = ["старт"]
        help_text = "̲С̲т̲а̲р̲т - возобновляет работу Петровича(только для админов). " \
                    "С параметром можно включить нужный модуль (синички, майн)"
        super().__init__(names, help_text, for_moderator=True)

    def start(self):
        if self.vk_event.args:
            if self.vk_event.args[0] == "синички":
                if not cameraHandler.is_active():
                    cameraHandler.resume()
                    self.vk_bot.send_message(self.vk_event.chat_id, "Стартуем синичек!")
                else:
                    self.vk_bot.send_message(self.vk_event.chat_id, "Синички уже стартовали")
            elif self.vk_event.args[0] in ["майн", "майнкрафт"]:
                do_the_linux_command('sudo systemctl start minecraft')
                self.vk_bot.send_message(self.vk_event.chat_id, "Стартуем майн!")
            else:
                self.vk_bot.send_message(self.vk_event.chat_id, "Не найден такой модуль")
        else:
            if not check_sender_admin(self.vk_bot, self.vk_event):
                return
            self.vk_bot.BOT_CAN_WORK = True
            self.vk_bot.send_message(self.vk_event.chat_id, "Стартуем!")
