from apps.API_VK.command.CommonCommand import CommonCommand, check_sender_admin
from apps.API_VK.command._DoTheLinuxComand import do_the_linux_command


class Restart(CommonCommand):
    def __init__(self):
        names = ["рестарт"]
        help_text = "̲Р̲е̲с̲т̲а̲р̲т - перезагружает веб-сервер и Петровича(только для админов). " \
                    "С параметром можно включить грузануть модуль (синички, майн)"
        super().__init__(names, help_text, for_moderator=True)

    def start(self):
        if self.vk_event.args:
            if self.vk_event.args[0] in ["майн", "майнкрафт"]:
                do_the_linux_command('sudo systemctl restart minecraft')
                self.vk_bot.send_message(self.vk_event.chat_id, "Рестартуем майн!")
            else:
                self.vk_bot.send_message(self.vk_event.chat_id, "Не найден такой модуль")
        else:
            if not check_sender_admin(self.vk_bot, self.vk_event):
                return

            self.vk_bot.send_message(self.vk_event.chat_id, "Внимание! Веб-сервер и Петрович будут перезагружены. "
                                                            "Встанету ли они - загадка. Желаю удачи")
            do_the_linux_command('sudo systemctl restart xoma163site')
