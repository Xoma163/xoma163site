from datetime import datetime

from django.core.management.base import BaseCommand

from apps.API_VK.models import VkUser
from apps.Statistics.models import Service
from xoma163site.wsgi import vk_bot


def check_server_by_info(ip, port, version):
    from apps.API_VK.command.commands.Status import get_minecraft_server_info
    res = get_minecraft_server_info(ip, port, version)
    stop_mine_by_version(res.find("запущен") != -1, res.find("Игроки") == -1, version)


def stop_mine_by_version(online, no_players, version):
    from apps.API_VK.command.CommonMethods import send_messages

    # Если сервак онлайн и нет игроков
    if online and no_players:
        from apps.API_VK.models import VkChat
        chat = VkChat.objects.get(chat_id=2000000001)

        obj, created = Service.objects.get_or_create(name=f'stop_minecraft_{version}')

        # Создание событие. Уведомление, что мы скоро всё отрубим
        if created:
            message = f"Если никто не зайдёт на сервак по майну {version}, то через полчаса я его остановлю"
            users_notify = VkUser.objects.filter(groups__name='minecraft_notify')
            send_messages(vk_bot, users_notify, message)

        # Если событие уже было создано, значит пора отрубать
        else:
            update_datetime = obj.update_datetime
            delta_seconds = (datetime.now() - update_datetime).seconds
            if delta_seconds <= 1800 + 100:
                obj.delete()
                Service.objects.get_or_create(name=f"minecraft_{version}")

                from apps.API_VK.command._DoTheLinuxComand import do_the_linux_command
                do_the_linux_command(f'sudo systemctl stop minecraft_{version}')

                vk_bot.send_message(chat.chat_id, f"Вырубаю майн {version}")
            else:
                obj.delete()

    # Эта ветка нужна, чтобы вручную вырубленные серверы не провоцировали при последующем старте отключение в 0/30 минут
    else:
        Service.objects.filter(name=f'stop_minecraft_{version}').delete()


class Command(BaseCommand):

    def handle(self, *args, **options):
        check_server_by_info("localhost", "25565", "1.12.2")
        check_server_by_info("localhost", "25566", "1.15.1")
