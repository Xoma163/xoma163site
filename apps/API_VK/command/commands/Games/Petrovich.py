import datetime
from threading import Lock

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import localize_datetime, remove_tz
from apps.games.models import PetrovichGames, PetrovichUser

lock = Lock()


class Petrovich(CommonCommand):
    def __init__(self):
        names = ["петрович", "женя"]
        help_text = "Петрович - мини-игра, определяющая кто Петрович Дня"
        detail_help_text = "Петрович - мини-игра, определяющая кто Петрович дня.\n" \
                           "Петрович рег - регистрация в игре\n" \
                           "Петрович дерег - дерегистрация в игре"
        super().__init__(names, help_text, detail_help_text, conversation=True)

    def start(self):
        if self.vk_event.args:
            if self.vk_event.args[0] == 'рег':
                p_user = PetrovichUser.objects.filter(user=self.vk_event.sender, chat=self.vk_event.chat).first()
                if p_user is not None:
                    if not p_user.active:
                        p_user.active = True
                        p_user.save()
                        return "Возвращаю тебя в строй"
                    else:
                        return "Ты уже зарегистрирован :)"
                min_wins = PetrovichUser.objects.filter(chat=self.vk_event.chat).aggregate(Min('wins'))['wins__min']

                p_user = PetrovichUser(user=self.vk_event.sender,
                                       chat=self.vk_event.chat,
                                       active=True)

                if min_wins:
                    p_user.wins = min_wins
                p_user.save()

                return "Регистрация прошла успешно"
            elif self.vk_event.args[0] == 'дерег':
                p_user = PetrovichUser.objects.filter(user=self.vk_event.sender, chat=self.vk_event.chat).first()
                if p_user is not None:
                    p_user.active = False
                    p_user.save()
                    return "Ок"
                else:
                    return "А ты и не зареган"
            return "не понял команды. /ман Петрович"
        with lock:
            winner_today = PetrovichGames.objects.filter(chat=self.vk_event.chat).last()
            if winner_today:
                datetime_now = localize_datetime(datetime.datetime.utcnow(), "Europe/Moscow")
                datetime_last = localize_datetime(remove_tz(winner_today.date), "Europe/Moscow")
                if (datetime_now.date() - datetime_last.date()).days <= 0:
                    if winner_today.user.name in ["Евгений", "Женя"]:
                        return f"Женя дня - {winner_today.user}"
                    elif winner_today.user.name in ["Светлана"]:
                        return f"Лапушка дня - {winner_today.user}"
                    else:
                        return f"Петрович дня - {winner_today.user}"

            winner = PetrovichUser.objects.filter(chat=self.vk_event.chat, active=True).order_by("?").first()
            if winner:
                winner = winner.user
            else:
                return "Нет участников игры. Зарегистрируйтесь! /рег"

            PetrovichGames.objects.filter(chat=self.vk_event.chat).delete()
            PetrovichGames(user=winner, chat=self.vk_event.chat).save()
            winner_petrovich = PetrovichUser.objects.filter(user=winner, chat=self.vk_event.chat).first()
            winner_petrovich.wins += 1
            winner_petrovich.save()
            messages = ["Такс такс такс, кто тут у нас"]
            who = "Петрович"
            if winner.name in ["Евгений", "Женя"]:
                who = "Женя"
            if winner.name in ["Светлана"]:
                messages.append(
                    f"Наша сегодняшняя лапушка дня - [{winner.nickname}|{winner.name} {winner.surname}]")
            else:
                messages.append(
                    f"Наш сегодняшний {who} дня - [{winner.nickname}|{winner.name} {winner.surname}]")
            return messages
