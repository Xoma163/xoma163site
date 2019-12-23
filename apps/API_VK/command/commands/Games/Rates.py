import random
from threading import Lock

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.games.models import Gamer
from apps.games.models import Rate as RateModel

MIN_GAMERS = 4

lock = Lock()


class Rates(CommonCommand):
    def __init__(self):
        names = ["ставки"]
        super().__init__(names, for_conversations=True)

    def start(self):
        lock.acquire()
        gamers = RateModel.objects.filter(chat=self.vk_event.chat).order_by("date")
        if len(gamers) < MIN_GAMERS:
            lock.release()
            return "Минимальное количество игроков - {}".format(MIN_GAMERS)
        messages = ["Ставки сделаны, ставок больше нет."]

        rnd = random.randint(1, 100)

        winner_rates = ([abs(rnd - gamer.rate) for gamer in gamers])
        min_val = min(winner_rates)
        winners = []
        for i, winner_rate in enumerate(winner_rates):
            if winner_rate == min_val:
                winners.append(gamers[i])

        winners_str = ""
        for winner in winners:
            gamer = Gamer.objects.get(user=winner.user)
            winners_str += "{}\n".format(gamer)

            if winner.rate != rnd:
                gamer.points += 1
            else:
                gamer.points += 5
                winners_str += "\nБонус +4 за точное попадание\n"

            gamer.save()

        if len(winners) == 1:
            msg = "Выпавшее число - {}\nПобедитель:\n{}".format(rnd, winners_str)
        else:
            msg = "Выпавшее число - {}\nПобедители:\n{}".format(rnd, winners_str)

        gamers.delete()
        messages.append(msg)
        lock.release()
        return messages
