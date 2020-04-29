from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.DoTheLinuxComand import do_the_linux_command


class Temperature(CommonCommand):
    def __init__(self):
        names = ["температура", "темп", "t"]
        help_text = "Температура - температуры сервера"
        super().__init__(names, help_text, access='moderator')

    def start(self):
        command = "sensors"
        output = do_the_linux_command(command)

        find_text = 'Adapter: ISA adapter\nPackage id 0:'
        output = f"AVG:{output[output.find(find_text) + len(find_text):].replace('(high = +80.0°C, crit = +100.0°C)', '')}"

        return output
