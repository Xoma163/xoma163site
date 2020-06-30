from apps.API_VK.APIs.Minecraft import servers_minecraft
from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.Consts import Role
from apps.API_VK.command.DoTheLinuxComand import do_the_linux_command
from xoma163site.settings import MAIN_DOMAIN


class Status(CommonCommand):
    def __init__(self):
        names = ["статус", "ранд"]
        help_text = "Статус - статус серверов по играм"
        keyboard = {'for': Role.MINECRAFT, 'text': 'Статус', 'color': 'green', 'row': 1, 'col': 1}
        super().__init__(names, help_text, int_args=[0, 1], keyboard=keyboard, access=Role.TRUSTED)

    def start(self):
        minecraft_result = ""
        for server in servers_minecraft:
            server.get_server_info()
            result = server.parse_server_info()
            minecraft_result += f"{result}\n\n"

        terraria = get_terraria_server_info("7777")

        total_str = f"{minecraft_result}" \
                    f"{terraria}"

        return total_str


def get_terraria_server_info(port):
    command = "systemctl status terraria"
    response = do_the_linux_command(command)
    index1 = response.find("Active: ") + len("Active: ")
    index2 = response.find("(", index1) - 1
    status = response[index1:index2]
    if status == 'active':
        result = f"Террария запущена ✅ - {MAIN_DOMAIN}:{port}\n"
    else:
        result = "Террария остановлена ⛔"

    return result
