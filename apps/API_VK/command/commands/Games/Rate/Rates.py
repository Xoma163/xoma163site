import random

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.games.models import Gamer
from apps.games.models import Rate as RateModel


class Rates(CommonCommand):
    def __init__(self):
        names = ["ставки"]
        super().__init__(names)

    def start(self):
        gamers = RateModel.objects.filter(chat=self.vk_event.chat)
        if len(gamers) < 2:
            self.vk_bot.send_message(self.vk_event.chat_id, "Для игры нужно хотя бы два игрока")
            return
        self.vk_bot.send_message(self.vk_event.chat_id, "Ставки сделаны, ставок больше нет.")

        rnd = random.randint(1, 100)

        min_delta = abs(rnd - gamers[0].rate)
        min_delta_index = 0
        for i, gamer in enumerate(gamers):
            if abs(rnd - gamer.rate) < min_delta:
                min_delta = gamer.rate
                min_delta_index = i

        winner = gamers[min_delta_index].user
        gamer = Gamer.objects.get(user=winner)
        gamer.points = int(gamer.points) + 1
        gamer.save()

        gamers.delete()
        self.vk_bot.send_message(self.vk_event.chat_id, "Выпавшее число - {}\nПобедитель - {}".format(rnd, gamer))
