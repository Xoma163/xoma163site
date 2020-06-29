from datetime import datetime

from django.core.management.base import BaseCommand

from apps.API_VK.VkBotClass import VkBotClass
from apps.API_VK.command.CommonMethods import remove_tz
from apps.API_VK.command.Consts import Role
from apps.API_VK.command.commands.TrustedCommands.Stop import stop_amazon_server
from apps.API_VK.models import VkUser
from apps.service.models import Service
from secrets.secrets import secrets

vk_bot = VkBotClass()


# ToDo: Говнокодище пиздец

def check_server_by_info(ip, port, version, amazon=False):
    from apps.API_VK.command.commands.TrustedCommands.Status import get_minecraft_server_info
    res = get_minecraft_server_info(ip, port, version)
    stop_mine_by_version(res.find("запущен") != -1, res.find("Игроки") == -1, version, amazon)


def stop_mine_by_version(online, no_players, version, amazon=False):
    # Если сервак онлайн и нет игроков
    if online and no_players:
        obj, created = Service.objects.get_or_create(name=f'stop_minecraft_{version}')

        # Создание событие. Уведомление, что мы скоро всё отрубим
        if created:
            message = f"Если никто не зайдёт на сервак по майну {version}, то через полчаса я его остановлю"
            users_notify = VkUser.objects.filter(groups__name=Role.MINECRAFT_NOTIFY.name)
            users_chat_id_notify = [user.user_id for user in users_notify]
            vk_bot.parse_and_send_msgs_thread(users_chat_id_notify, message)

        # Если событие уже было создано, значит пора отрубать
        else:
            update_datetime = obj.update_datetime
            delta_seconds = (datetime.utcnow() - remove_tz(update_datetime)).seconds
            if delta_seconds <= 1800 + 100:
                obj.delete()
                Service.objects.get_or_create(name=f"minecraft_{version}")

                if amazon:
                    stop_amazon_server(secrets['minecraft-amazon']['ip'], secrets['minecraft-amazon']['port'])
                else:
                    from apps.API_VK.command.DoTheLinuxComand import do_the_linux_command
                    do_the_linux_command(f'sudo systemctl stop minecraft_{version}')

                message = f"Вырубаю майн {version}"
                users_notify = VkUser.objects.filter(groups__name=Role.MINECRAFT_NOTIFY.name)
                users_chat_id_notify = [user.user_id for user in users_notify]
                vk_bot.parse_and_send_msgs_thread(users_chat_id_notify, message)
            else:
                obj.delete()

    # Эта ветка нужна, чтобы вручную вырубленные серверы не провоцировали при последующем старте отключение в 0/30 минут
    else:
        Service.objects.filter(name=f'stop_minecraft_{version}').delete()


class Command(BaseCommand):

    def handle(self, *args, **options):
        check_server_by_info("localhost", "25565", "1.12.2")
        check_server_by_info("localhost", "25566", "1.15.1")
        check_server_by_info(secrets['minecraft-amazon']['ip'], secrets['minecraft-amazon']['port'], "1.16.1",
                             amazon=True)
