from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command._DoTheLinuxComand import do_the_linux_command


class Temperature(CommonCommand):
    def __init__(self):
        names = ["температура", "темп", "t"]
        help_text = "̲Т̲е̲м̲п̲е̲р̲а̲т̲у̲р̲а - температуры сервера"
        super().__init__(names, help_text, for_moderator=True)

    def start(self):
        command = "sensors"
        output = do_the_linux_command(command)

        find_text = 'Adapter: ISA adapter\nPackage id 0:'
        output = "AVG:" + output[output.find(find_text) + len(find_text):].replace(" (high = +80.0°C, crit = +100.0°C)",
                                                                                   '')

        self.vk_bot.send_message(self.vk_event.chat_id, output)
