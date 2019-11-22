import datetime
import random

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.models import PetrovichGames, PetrovichUser


class Petrovich(CommonCommand):
    def __init__(self):
        names = ["петрович"]
        super().__init__(names, for_conversations=True)

    def start(self):
        today = datetime.datetime.now()
        winner_today = PetrovichGames.objects.filter(date__year=today.year,
                                                     date__month=today.month,
                                                     date__day=today.day,
                                                     chat_id=self.vk_event.chat_id).last()
        if winner_today is not None:
            self.vk_bot.send_message(self.vk_event.chat_id, "Петрович дня - %s" % winner_today.user)
            return

        users = PetrovichUser.objects.filter(chat_id=self.vk_event.chat_id)
        random_int = random.randint(0, len(users) - 1)
        winner = users[random_int].user
        PetrovichGames.objects.filter(chat_id=self.vk_event.chat_id).delete()
        new_winner = PetrovichGames()
        new_winner.user = winner
        new_winner.chat_id = self.vk_event.chat_id
        new_winner.save()
        winner_petrovich = PetrovichUser.objects.filter(user=winner).first()
        winner_petrovich.wins += 1
        winner_petrovich.save()
        self.vk_bot.send_message(self.vk_event.chat_id, "Такс такс такс, кто тут у нас")
        self.vk_bot.send_message(self.vk_event.chat_id, "Наш сегодняшний Петрович дня - %s" % winner)
