import datetime
import json
import random
from threading import Lock

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import random_event, localize_datetime, remove_tz
from apps.games.models import RouletteRate, Gamer

# Кратно 12
MAX_NUMBERS = 36

lock = Lock()


# By E.Dubovitsky
def is_red(n):
    j = (n - 1) % 9  # номер в квадратике
    i = (n - 1) / 9  # номер самого квадратика

    j_even = j % 2 == 0  # попадает ли номер внутри квадратика в крестик
    i_even = i % 2 == 0  # чётный ли сам квадратик

    return j_even and (i_even or j != 0)


def generate_translator():
    translator_numbers = {str(i): {'win_numbers': [i], 'coefficient': MAX_NUMBERS, 'verbose_name': i} for i in
                          range(MAX_NUMBERS + 1)}
    translator = {
        'красное': {'win_numbers': [i for i in range(1, MAX_NUMBERS + 1) if is_red(i)], 'coefficient': 2,
                    'verbose_name': "красное"},
        'черное': {'win_numbers': [i for i in range(1, MAX_NUMBERS + 1) if not is_red(i)], 'coefficient': 2,
                   'verbose_name': "чёрное"},
        'строка': {1: {'win_numbers': [i for i in range(3, MAX_NUMBERS + 1, 3)], 'coefficient': 3,
                       'verbose_name': "1я строка"},
                   2: {'win_numbers': [i for i in range(2, MAX_NUMBERS, 3)], 'coefficient': 3,
                       'verbose_name': "2 строка"},
                   3: {'win_numbers': [i for i in range(1, MAX_NUMBERS, 3)], 'coefficient': 3,
                       'verbose_name': "3 строка"},
                   },
        'столбец': {1: {'win_numbers': [i for i in range(1, MAX_NUMBERS // 3 + 1)], 'coefficient': 3,
                        'verbose_name': "1 столбец"},
                    2: {'win_numbers': [i for i in range(MAX_NUMBERS // 3 + 1, MAX_NUMBERS * 2 // 3 + 1)],
                        'coefficient': 3, 'verbose_name': "2 столбец"},
                    3: {'win_numbers': [i for i in range(MAX_NUMBERS * 2 // 3 + 1, MAX_NUMBERS + 1)], 'coefficient': 3,
                        'verbose_name': "3 столбец"},
                    },
        'первая': {'win_numbers': [i for i in range(1, MAX_NUMBERS // 2 + 1)], 'coefficient': 2,
                   'verbose_name': "первая половина"},
        'вторая': {'win_numbers': [i for i in range(MAX_NUMBERS // 2 + 1, MAX_NUMBERS + 1)], 'coefficient': 2},
        'verbose_name': "вторая половина",
        'четное': {'win_numbers': [i for i in range(2, MAX_NUMBERS + 1, 2)], 'coefficient': 2,
                   'verbose_name': "чётное"},
        'нечетное': {'win_numbers': [i for i in range(1, MAX_NUMBERS, 2)], 'coefficient': 2,
                     'verbose_name': "нечётное"},
    }

    translator.update(translator_numbers)

    return translator


TRANSLATOR = generate_translator()


# def str_is_int(rate):
#     try:
#         int(rate)
#         return True
#     except ValueError:
#         return False


class Roulette(CommonCommand):
    def __init__(self):
        names = ["рулетка"]
        help_text = "Рулетка - рулетка"
        detail_help_text = "/рулетка - запуск рулетки\n" \
                           "/рулетка {аргументы} {ставка}- ставка рулетки\n" \
                           f"/рулетка 0-{MAX_NUMBERS} - ставка на число\n" \
                           "/рулетка столбец (1,2,3) - ставка на столбец\n" \
                           "/рулетка строка (1,2,3) - ставка на строку\n" \
                           "/рулетка красное/чёрное - ставка на цвет\n" \
                           "/рулетка чётное/нечётное - ставка на кратность\n" \
                           "/рулетка первая/вторая - ставка на 1/2 части стола\n" \
                           "\n" \
                           "рулетка баланс [игрок] - баланс [игрока]\n" \
                           "рулетка картинка - картинка рулетки\n" \
                           "рулетка бонус - получение пособия по безработице\n" \
                           "рулетка передать [игрок] очки - передача очков другому игроку\n"

        super().__init__(names, help_text, detail_help_text, conversation=True)

    def start(self):
        if self.vk_event.args:

            if len(Gamer.objects.filter(user=self.vk_event.sender)) == 0:
                Gamer(user=self.vk_event.sender).save()
            gamer = Gamer.objects.filter(user=self.vk_event.sender).first()

            if self.vk_event.args[0] == 'баланс':
                if len(self.vk_event.args) > 1:
                    username = " ".join(self.vk_event.args[1:])
                    vk_user = self.vk_bot.get_user_by_name(username, self.vk_event.chat)
                    vk_user_gamer = Gamer.objects.filter(user=vk_user).first()
                    if not vk_user_gamer:
                        return "Не нашёл такого игрока"
                    return f"Баланс игрока {vk_user} - {vk_user_gamer.roulette_points}"
                else:
                    return f"Ваш баланс - {gamer.roulette_points}"
            if self.vk_event.args[0] == 'картинка':
                attachment = random_event(
                    [self.vk_bot.get_photo_by_id(457242125), self.vk_bot.get_photo_by_id(457242126)], [90, 10])
                return {'attachments': attachment}
            if self.vk_event.args[0] == 'бонус':
                datetime_now = localize_datetime(datetime.datetime.utcnow(), "Europe/Moscow")
                datetime_last = localize_datetime(remove_tz(gamer.roulette_points_today), "Europe/Moscow")
                if gamer.roulette_points > 10000:
                    return "Тебе хватит и так"
                if (datetime_now.date() - datetime_last.date()).days > 0:
                    gamer.roulette_points += 500
                    gamer.roulette_points_today = datetime_now
                    gamer.save()
                    return "Выдал пособие по безработице"
                else:
                    return "Приходи завтра"
            if self.vk_event.args[0] in ['передать', 'перевод', 'перевести', 'подать']:
                self.args = 3
                self.int_args = [-1]
                self.check_args()
                self.parse_args('int')

                points_transfer = self.vk_event.args[-1]
                if points_transfer > gamer.roulette_points:
                    return "Недостаточно очков"
                if points_transfer <= 0:
                    return "Очков должно быть >0"
                username = " ".join(self.vk_event.args[1:-1])
                vk_user = self.vk_bot.get_user_by_name(username, self.vk_event.chat)
                vk_user_gamer = Gamer.objects.filter(user=vk_user).first()
                if not vk_user_gamer:
                    return "Не нашёл такого игрока"

                if gamer == vk_user_gamer:
                    return "))"

                gamer.roulette_points -= points_transfer
                gamer.save()
                vk_user_gamer.roulette_points += points_transfer
                vk_user_gamer.save()
                return f"Передал игроку {vk_user_gamer.user} {points_transfer} очков"
            if self.vk_event.args[0] in ['ставки']:
                rrs = RouletteRate.objects.filter(chat=self.vk_event.chat)
                msg = ""
                for rr in rrs:
                    rate_on_dict = json.loads(rr.rate_on)
                    msg += f"{rr.gamer.user} поставил на {rate_on_dict['verbose_name']} {rr.rate} очков\n"
                return msg
            rate_on = self.vk_event.args[0]
            # rate_is_int = str_is_int(rate_on)
            if rate_on in TRANSLATOR:  # or rate_is_int:
                self.args = 2
                self.check_args()
                if self.vk_event.args[-1].lower() == 'все':
                    rate = gamer.roulette_points
                else:
                    self.int_args = [-1]
                    self.parse_args('int')
                    rate = self.vk_event.args[-1]
                if rate <= 0:
                    return "Ставка не может быть ⩽0"
                if rate > gamer.roulette_points:
                    return f"Ставка не может быть больше ваших очков - {gamer.roulette_points}"

                if rate_on in ['строка', 'столбец']:
                    self.args = 3
                    self.int_args = [1, 2]
                    self.check_args()
                    self.parse_args('int')
                    rowcol = self.vk_event.args[1]
                    self.check_number_arg_range(rowcol, 1, 3)

                    rate_obj = TRANSLATOR[rate_on][rowcol]

                # elif rate_is_int:
                #     rate_obj = {'win_numbers': [int(rate_on)], 'coefficient': MAX_NUMBERS}
                else:
                    rate_obj = TRANSLATOR[rate_on]
                rr = RouletteRate(gamer=gamer, chat=self.vk_event.chat, rate_on=json.dumps(rate_obj), rate=rate)
                rr.save()
                gamer.roulette_points -= rate
                gamer.save()

                return "Поставил"

            else:
                return "Не могу понять на что вы поставили. /ман рулетка"
        else:
            with lock:
                rrs = RouletteRate.objects.filter(chat=self.vk_event.chat)
                if len(rrs) == 0:
                    return "Ставок нет"
                msg1 = "Ставки сделаны. Ставок больше нет\n"
                roulette_ball = random.randint(0, MAX_NUMBERS)
                msg2 = f"Крутим колесо. Выпало - {roulette_ball}\n\n"

                winners = []
                for rr in rrs:
                    rate_on = json.loads(rr.rate_on)
                    if roulette_ball in rate_on['win_numbers']:
                        win_points = rr.rate * rate_on['coefficient']
                        rr.gamer.roulette_points += win_points
                        rr.gamer.save()
                        winners.append({'user': rr.gamer.user, 'points': win_points})
                if len(winners) > 0:
                    msg3 = "Победители:\n"
                    for winner in winners:
                        msg3 += f"{winner['user']} - {winner['points']}\n"
                else:
                    msg3 = "Нет победителей"
                msg = msg1 + msg2 + msg3
                rrs.delete()
                return msg
