from datetime import datetime

from django.core.management.base import BaseCommand

from apps.Statistics.models import Service
from xoma163site.wsgi import vk_bot


def stop_mine_by_version(online, no_players, version):
    # Если сервак онлайн и нет игроков
    if online and no_players:
        from apps.API_VK.models import VkChat
        chat = VkChat.objects.get(chat_id=2000000002)

        obj, created = Service.objects.get_or_create(name=f'stop_minecraft_{version}')

        # Создание событие. Уведомление, что мы скоро всё отрубим
        if created:
            vk_bot.send_message(chat.chat_id,
                                f"Если никто не зайдёт на сервак по майну {version}, то через полчаса я его остановлю")

        # Если событие уже было создано, значит пора отрубать
        else:
            update_datetime = obj.update_datetime
            delta_seconds = (datetime.now() - update_datetime).seconds
            if delta_seconds <= 1800 + 100:
                obj.delete()
                vk_bot.send_message(chat.chat_id, f"Вырубаю майн {version}")
            else:
                obj.delete()

    # Эта ветка нужна, чтобы вручную вырубленные серверы не провоцировали при последующем старте отключение в 0/30 минут
    else:
        Service.objects.filter(name=f'stop_minecraft_{version}').delete()


class Command(BaseCommand):

    def handle(self, *args, **options):
        from apps.API_VK.command.commands.Status import get_minecraft_server_info

        res_1_12 = get_minecraft_server_info("192.168.1.10", "25565", "1.12.2")
        stop_mine_by_version(res_1_12.find("запущен") != -1, res_1_12.find("Игроки") == -1, "1.12.2")
        res_1_15_1 = get_minecraft_server_info("192.168.1.10", "25566", "1.15.1")
        stop_mine_by_version(res_1_15_1.find("запущен") != -1, res_1_15_1.find("Игроки") == -1, "1.15.1")
