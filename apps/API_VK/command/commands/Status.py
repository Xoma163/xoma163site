import json

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command._DoTheLinuxComand import do_the_linux_command
from xoma163site.settings import MAIN_DOMAIN


class Status(CommonCommand):
    def __init__(self):
        names = ["статус", "ранд"]
        help_text = "̲С̲т̲а̲т̲у̲с - статус серверов по играм"
        keyboard = {'for': 'minecraft', 'text': 'Статус', 'color': 'green', 'row': 1, 'col': 1}
        super().__init__(names, help_text, check_int_args=[0, 1], keyboard=keyboard)

    # ToDo: не работает с внешним адресом
    def start(self):
        res_1_12 = get_minecraft_server_info("192.168.1.10", "25565", "1.12.2")
        res_1_15_1 = get_minecraft_server_info("192.168.1.10", "25566", "1.15.1")
        terraria = get_terraria_server_info("192.168.1.10", "7777", "хз")

        total_str = "{}\n\n{}\n\n{}".format(res_1_12, res_1_15_1, terraria)

        return total_str


def get_minecraft_server_info(ip, port, v):
    command = "/var/www/xoma163.site/venv/bin/mcstatus {}:{} json".format(ip, port)
    response = json.loads(do_the_linux_command(command))
    if not response['online']:
        result = "Майн {} - остановлен".format(v)
    else:
        players = " ".join(player['name'] for player in response['players'])
        result = "Майн {} - запущен ({}/{}) - {}:{}\n".format(response['version'], response['player_count'],
                                                              response['player_max'], MAIN_DOMAIN, port)
        if len(players) > 0:
            result += "Игроки: {}".format(players)
    return result


def get_terraria_server_info(ip, port, v):
    command = "systemctl status terraria"
    response = do_the_linux_command(command)
    index1 = response.find("Active: ") + len("Active: ")
    index2 = response.find("(", index1) - 1
    status = response[index1:index2]
    if status == 'active':
        result = "Террария запущена - {}:{}\n".format(MAIN_DOMAIN, port)
    else:
        result = "Террария остановлена".format(v)

    return result
