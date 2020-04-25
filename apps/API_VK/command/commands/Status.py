import json

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command._DoTheLinuxComand import do_the_linux_command
from xoma163site.settings import MAIN_DOMAIN


class Status(CommonCommand):
    def __init__(self):
        names = ["статус", "ранд"]
        help_text = "Статус - статус серверов по играм"
        keyboard = {'for': 'minecraft', 'text': 'Статус', 'color': 'green', 'row': 1, 'col': 1}
        super().__init__(names, help_text, int_args=[0, 1], keyboard=keyboard)

    def start(self):
        res_1_12 = get_minecraft_server_info("localhost", "25565", "1.12.2")
        res_1_15_1 = get_minecraft_server_info("localhost", "25566", "1.15.1")
        terraria = get_terraria_server_info("localhost", "7777", "хз")

        total_str = f"{res_1_12}\n\n" \
                    f"{res_1_15_1}\n\n" \
                    f"{terraria}"

        return total_str


def get_minecraft_server_info(ip, port, v):
    command = f"/var/www/xoma163.site/venv/bin/mcstatus {ip}:{port} json"
    response = json.loads(do_the_linux_command(command))
    if not response['online']:
        result = f"Майн {v} - остановлен ⛔"
    else:
        players = " ".join(player['name'] for player in response['players'])
        result = f"Майн {response['version']} - запущен ✅ ({response['player_count']}/{response['player_max']}) - {MAIN_DOMAIN}:{port}\n"
        if len(players) > 0:
            result += f"Игроки: {players}"
    return result


def get_terraria_server_info(ip, port, v):
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
