import random

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.games.models import Gamer
from apps.games.models import Rate as RateModel


class Rates(CommonCommand):
    def __init__(self):
        names = ["ставки"]
        super().__init__(names, for_conversations=True)

    def start(self):
        gamers = RateModel.objects.filter(chat=self.vk_event.chat).order_by("date")
        if len(gamers) < 2:
            self.vk_bot.send_message(self.vk_event.chat_id, "Для игры нужно хотя бы два игрока")
            return
        self.vk_bot.send_message(self.vk_event.chat_id, "Ставки сделаны, ставок больше нет.")

        rnd = random.randint(1, 100)

        winner_rates = ([abs(rnd - gamer.rate) for gamer in gamers])
        winner = gamers[winner_rates.index(min(winner_rates))]

        gamer = Gamer.objects.get(user=winner.user)
        gamer.points = int(gamer.points) + 1

        self.vk_bot.send_message(self.vk_event.chat_id, "Выпавшее число - {}\nПобедитель - {}".format(rnd, gamer))

        if winner.rate == rnd:
            gamer.points = int(gamer.points) + 2
            self.vk_bot.send_message(self.vk_event.chat_id, "Бонус +2 очка за точное попадание")

        gamer.save()
        gamers.delete()
