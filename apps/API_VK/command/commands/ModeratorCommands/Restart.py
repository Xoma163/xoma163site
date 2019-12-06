from apps.API_VK.command.CommonCommand import CommonCommand, check_sender_admin, check_sender_minecraft, \
    check_command_time
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
                if not check_sender_minecraft(self.vk_bot, self.vk_event):
                    return
                if len(self.vk_event.args) >= 2:
                    if self.vk_event.args[1] == '1.12':
                        if not check_command_time(self.vk_bot, self.vk_event, 'minecraft 1.12', 90):
                            return

                        do_the_linux_command('sudo systemctl start minecraft')
                        self.vk_bot.send_message(self.vk_event.chat_id, "Рестартим майн 1.12!")
                    elif self.vk_event.args[1] == '1.15':
                        if not check_command_time(self.vk_bot, self.vk_event, 'minecraft 1.15', 90):
                            return

                        do_the_linux_command('sudo systemctl start minecraft_1_15')
                        self.vk_bot.send_message(self.vk_event.chat_id, "Рестартим майн 1.15!")
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

            self.vk_bot.send_message(self.vk_event.chat_id, "Внимание! Веб-сервер и Петрович будут перезагружены. "
                                                            "Встанету ли они - загадка. Желаю удачи")
            do_the_linux_command('sudo systemctl restart xoma163site')
