import time

import requests
from mcrcon import MCRcon

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.Consts import Role
from apps.API_VK.command.DoTheLinuxComand import do_the_linux_command
from apps.API_VK.models import VkUser
from apps.birds.CameraHandler import CameraHandler
from apps.service.models import Service
from secrets.secrets import secrets

cameraHandler = CameraHandler()


class Stop(CommonCommand):
    def __init__(self):
        names = ["стоп", "stop"]
        help_text = "Стоп - останавливает работу бота или модуля"
        detail_help_text = "Стоп [сервис=бот [версия=1.15.1]] - останавливает сервис\n" \
                           "Сервис - бот/синички/майнкрафт/террария\n" \
                           "Если майнкрафт, то может быть указана версия, 1.12.2 или 1.15.1"

        keyboard = [{'for': Role.ADMIN, 'text': 'Стоп', 'color': 'red', 'row': 1, 'col': 2},
                    {'for': Role.ADMIN, 'text': 'Стоп синички', 'color': 'red', 'row': 1, 'col': 4}]
        super().__init__(names, help_text, detail_help_text, keyboard=keyboard, access=Role.TRUSTED)

    def start(self):
        module = "bot"
        if self.vk_event.args:
            module = self.vk_event.args[0].lower()
        if module in ["синички"]:
            self.check_sender(Role.ADMIN)
            if cameraHandler.is_active():
                cameraHandler.terminate()
                return "Финишируем синичек"
            else:
                return "Синички уже финишировали"
        elif module in ["майн", "майнкрафт", "mine", "minecraft"]:
            self.check_sender(Role.MINECRAFT)
            if len(self.vk_event.args) >= 2 and (
                    self.vk_event.args[1] == '1.12' or self.vk_event.args[1] == '1.12.2'):
                self.check_command_time('minecraft_1.12', 90)

                do_the_linux_command('sudo systemctl stop minecraft_1.12.2')
                Service.objects.filter(name='stop_minecraft_1.12.2').delete()

                message = "Финишируем майн 1.12!"
                users_notify = VkUser.objects.filter(groups__name=Role.MINECRAFT_NOTIFY.name) \
                    .exclude(id=self.vk_event.sender.id)
                users_chat_id_notify = [user.user_id for user in users_notify]
                self.vk_bot.parse_and_send_msgs_thread(users_chat_id_notify,
                                                       message + f"\nИнициатор - {self.vk_event.sender}")

                return message
            elif (len(self.vk_event.args) >= 2 and (
                    self.vk_event.args[1] == '1.15.1' or self.vk_event.args[1] == '1.15')):
                self.check_command_time('minecraft_1.15.1', 30)

                do_the_linux_command('sudo systemctl stop minecraft_1.15.1')
                Service.objects.filter(name='stop_minecraft_1.15.1').delete()

                message = "Финишируем майн 1.15.1"
                users_notify = VkUser.objects.filter(groups__name=Role.MINECRAFT_NOTIFY.name) \
                    .exclude(id=self.vk_event.sender.id)
                users_chat_id_notify = [user.user_id for user in users_notify]
                self.vk_bot.parse_and_send_msgs_thread(users_chat_id_notify,
                                                       message + f"\nИнициатор - {self.vk_event.sender}")

                return message
            elif (len(self.vk_event.args) >= 2 and (
                    self.vk_event.args[1] == '1.16.1' or self.vk_event.args[1] == '1.16')) or len(
                self.vk_event.args) == 1:
                self.check_command_time('minecraft_1.16.1', 30)

                stop_amazon_server(secrets['minecraft-amazon']['ip'])
                Service.objects.filter(name='stop_minecraft_1.16.1').delete()

                message = "Финишируем сервер майна 1.16.1"
                users_notify = VkUser.objects.filter(groups__name=Role.MINECRAFT_NOTIFY.name) \
                    .exclude(id=self.vk_event.sender.id)
                users_chat_id_notify = [user.user_id for user in users_notify]
                self.vk_bot.parse_and_send_msgs_thread(users_chat_id_notify,
                                                       message + f"\nИнициатор - {self.vk_event.sender}")

                return message
            else:
                return "Я не знаю такой версии"
        elif module in ['террария', 'terraria']:
            self.check_sender(Role.TERRARIA)
            self.check_command_time('terraria', 10)
            do_the_linux_command('sudo systemctl stop terraria')
            return "Финишируем террарию!"
        elif module in ['бот', 'bot']:
            self.check_sender(Role.ADMIN)
            self.vk_bot.BOT_CAN_WORK = False
            cameraHandler.terminate()
            return "Финишируем"
        else:
            return "Не найден такой модуль"


def send_rcon(ip, command):
    try:
        with MCRcon(ip, secrets['minecraft-amazon']['rcon_password']) as mcr:
            resp = mcr.command(command)
            if resp:
                return resp
            else:
                return False
    except:
        return False


def stop_amazon_server(ip):
    send_rcon(ip, '/stop')

    while True:
        server_is_offline = not send_rcon(ip, '/help')
        if server_is_offline:
            break
        time.sleep(5)

    URL = secrets['minecraft-amazon']['stop_url']
    requests.post(URL)
