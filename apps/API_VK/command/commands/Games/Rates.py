import random
from threading import Lock

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.models import VkUser
from apps.games.models import Rate as RateModel

lock = Lock()


class Rates(CommonCommand):
    def __init__(self):
        names = ["ставки", "казино"]
        help_text = "Ставки - играет ставки"
        detail_help_text = "Ставки - играет ставки. Если передан f последним параметром, то играет независимо от " \
                           "количества игроков"

        super().__init__(names, help_text, detail_help_text, conversation=True)

    def start(self):
        with lock:

            MIN_GAMERS = int(len(VkUser.objects.filter(chats=self.vk_event.chat)) / 2)
            if MIN_GAMERS < 2:
                MIN_GAMERS = 2

            gamers = RateModel.objects.filter(chat=self.vk_event.chat).order_by("date")
            if self.vk_event.args and self.vk_event.args[0] == 'f':
                self.check_sender('admin')
                if len(gamers) < 1:
                    return "Ну ты ваще обалдел? Хотя бы один игрок-то пусть будет"


            else:
                if len(gamers) < MIN_GAMERS:
                    return f"Минимальное количество игроков - {MIN_GAMERS}"
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
                gamer = self.vk_bot.get_gamer_by_user(self.vk_event.sender)
                winners_str += f"{gamer}\n"

                if winner.rate != rnd:
                    gamer.points += 1
                else:
                    gamer.points += 5
                    winners_str += "\nБонус x5 за точное попадание\n"

                gamer.save()

            if self.vk_event.command == "казино":
                attachments = []
                photo = self.vk_bot.get_attachment_by_id('photo', None, 457241180)
                attachments.append(photo)
                if len(winners) == 1:
                    msg = {'msg': f"Выпавшее число - {rnd}\nПобедитель этого казино:\n{winners_str}",
                           'attachments': attachments}
                else:
                    msg = {'msg': f"Выпавшее число - {rnd}\nПобедители этого казино:\n{winners_str}",
                           'attachments': attachments}
            else:
                if len(winners) == 1:
                    msg = f"Выпавшее число - {rnd}\nПобедитель:\n{winners_str}"
                else:
                    msg = f"Выпавшее число - {rnd}\nПобедители:\n{winners_str}"

            gamers.delete()
            messages.append(msg)
            return messages
