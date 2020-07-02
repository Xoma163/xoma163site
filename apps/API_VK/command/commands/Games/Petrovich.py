import datetime
from threading import Lock

from django.db.models import Min

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import localize_datetime, remove_tz
from apps.games.models import PetrovichGames, PetrovichUser

lock = Lock()


class Petrovich(CommonCommand):
    def __init__(self):
        names = ["петрович"]
        help_text = "Петрович - мини-игра, определяющая кто Петрович Дня"
        detail_help_text = "Петрович - мини-игра, определяющая кто Петрович дня\n" \
                           "Петрович рег - регистрация в игре\n" \
                           "Петрович дерег - дерегистрация в игре"
        super().__init__(names, help_text, detail_help_text, conversation=True)

    def start(self):
        if self.vk_event.args:
            arg0 = self.vk_event.args[0].lower()
        else:
            arg0 = None
        menu = [
            [['рег', 'регистрация'], self.menu_reg],
            [['дерег'], self.menu_dereg],
            [['default'], self.menu_play]
        ]
        method = self.handle_menu(menu, arg0)
        return method()

    def menu_reg(self):
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

    def menu_dereg(self):
        p_user = PetrovichUser.objects.filter(user=self.vk_event.sender, chat=self.vk_event.chat).first()
        if p_user is not None and p_user.active:
            p_user.active = False
            p_user.save()
            return "Ок"
        else:
            return "А ты и не зареган"

    def menu_play(self):
        with lock:
            winner_today = PetrovichGames.objects.filter(chat=self.vk_event.chat).last()
            if winner_today:
                datetime_now = localize_datetime(datetime.datetime.utcnow(), "Europe/Moscow")
                datetime_last = localize_datetime(remove_tz(winner_today.date), "Europe/Moscow")
                if (datetime_now.date() - datetime_last.date()).days <= 0:
                    if winner_today.user.gender == '1':
                        winner_gender = "Петровна"
                    else:
                        winner_gender = "Петрович"
                    return f"{winner_gender} дня - {winner_today.user}"

            winner = PetrovichUser.objects.filter(chat=self.vk_event.chat, active=True).order_by("?").first()
            if winner:
                winner = winner.user
            else:
                return "Нет участников игры. Зарегистрируйтесь! /петрович рег"

            PetrovichGames.objects.filter(chat=self.vk_event.chat).delete()
            PetrovichGames(user=winner, chat=self.vk_event.chat).save()
            winner_petrovich = PetrovichUser.objects.filter(user=winner, chat=self.vk_event.chat).first()
            winner_petrovich.wins += 1
            winner_petrovich.save()
            if winner_petrovich.user.gender == '1':
                winner_gender = "Наша сегодняшняя Петровна дня"
            else:
                winner_gender = "Наш сегодняшний Петрович дня"
            messages = ["Такс такс такс, кто тут у нас",
                        f"{winner_gender} - [{winner.nickname}|{winner.name} {winner.surname}]"]
            return messages
