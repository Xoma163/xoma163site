import datetime
from threading import Lock

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.games.models import PetrovichGames, PetrovichUser

lock = Lock()


class Petrovich(CommonCommand):
    def __init__(self):
        names = ["петрович", "женя"]
        help_text = "Петрович - мини-игра, определяющая кто Петрович Дня"
        detail_help_text = "Петрович - мини-игра, определяющая кто Петрович дня. Для участия нужно зарегистрироваться /рег"
        super().__init__(names, help_text, detail_help_text, conversation=True)

    def start(self):
        with lock:
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
            messages.append(
                f"Наш сегодняшний {who} дня - [{winner.nickname}|{winner.name} {winner.surname}]")
            return messages
