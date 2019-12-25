import datetime

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.games.models import PetrovichGames, PetrovichUser


class Petrovich(CommonCommand):
    def __init__(self):
        names = ["петрович", "женя"]
        help_text = "̲П̲е̲т̲р̲о̲в̲и̲ч - мини-игра, определяющая кто Петрович Дня"
        super().__init__(names, help_text, for_conversations=True)

    def start(self):
        today = datetime.datetime.now()
        winner_today = PetrovichGames.objects.filter(date__year=today.year,
                                                     date__month=today.month,
                                                     date__day=today.day,
                                                     chat=self.vk_event.chat).last()
        if winner_today is not None:
            if winner_today.user.name in ["Евгений", "Женя"]:
                return "Женя дня - %s" % winner_today.user
            else:
                return "Петрович дня - %s" % winner_today.user

        # order_by ? = random
        winner = PetrovichUser.objects.filter(chat=self.vk_event.chat, active=True).order_by("?").first()
        if winner:
            winner = winner.user
        else:
            return "Нет участников игры. Зарегистрируйтесь! /рег"

        PetrovichGames.objects.filter(chat=self.vk_event.chat).delete()
        new_winner = PetrovichGames()
        new_winner.user = winner
        new_winner.chat = self.vk_event.chat
        new_winner.save()
        winner_petrovich = PetrovichUser.objects.filter(user=winner, chat=self.vk_event.chat).first()
        winner_petrovich.wins = int(winner_petrovich.wins) + 1
        winner_petrovich.save()
        messages = ["Такс такс такс, кто тут у нас"]
        who = "Петрович"
        if winner.name in ["Евгений", "Женя"]:
            who = "Женя"
        messages.append("Наш сегодняшний {} дня - [{}|{} {}]".format(who, winner.nickname, winner.name, winner.surname))
        return messages