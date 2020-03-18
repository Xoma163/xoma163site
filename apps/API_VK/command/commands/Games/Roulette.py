import json
import random
from threading import Lock

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.games.models import RouletteRate, Gamer

# Кратно трём
MAX_NUMBERS = 36

lock = Lock()


def is_red(n):
    j = (n - 1) % 9  # номер в квадратике
    i = (n - 1) / 9  # номер самого квадратика

    j_even = j % 2 == 0  # попадает ли номер внутри квадратика в крестик
    i_even = i % 2 == 0  # чётный ли сам квадратик

    return j_even and (i_even or j != 0)


def generate_translator():
    translator_numbers = {str(i): {'win_numbers': [i], 'coefficient': MAX_NUMBERS} for i in range(MAX_NUMBERS + 1)}
    translator = {
        'красное': {'win_numbers': [], 'coefficient': 2},
        'черное': {'win_numbers': [], 'coefficient': 2},
        'строка': {1: {'win_numbers': [i for i in range(3, MAX_NUMBERS + 1, 3)], 'coefficient': 3},
                   2: {'win_numbers': [i for i in range(2, MAX_NUMBERS, 3)], 'coefficient': 3},
                   3: {'win_numbers': [i for i in range(1, MAX_NUMBERS, 3)], 'coefficient': 3},
                   },
        'столбец': {1: {'win_numbers': [i for i in range(1, MAX_NUMBERS // 3 + 1)], 'coefficient': 3},
                    2: {'win_numbers': [i for i in range(MAX_NUMBERS // 3 + 1, MAX_NUMBERS * 2 // 3 + 1)],
                        'coefficient': 3},
                    3: {'win_numbers': [i for i in range(MAX_NUMBERS * 2 // 3 + 1, MAX_NUMBERS + 1)], 'coefficient': 3},
                    },
        'первая': {'win_numbers': [i for i in range(1, MAX_NUMBERS // 2 + 1)], 'coefficient': 2},
        'вторая': {'win_numbers': [i for i in range(MAX_NUMBERS // 2 + 1, MAX_NUMBERS + 1)], 'coefficient': 2},
        'четное': {'win_numbers': [i for i in range(2, MAX_NUMBERS + 1, 2)], 'coefficient': 2},
        'нечетное': {'win_numbers': [i for i in range(1, MAX_NUMBERS, 2)], 'coefficient': 2},
    }

    translator.update(translator_numbers)

    red_numbers = []
    black_numbers = []
    for i in range(1, MAX_NUMBERS + 1):
        if is_red(i):
            red_numbers.append(i)
        else:
            black_numbers.append(i)
    translator['красное']['win_numbers'] = red_numbers
    translator['черное']['win_numbers'] = black_numbers

    return translator


TRANSLATOR = generate_translator()


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
                           "/рулетка первая/вторая - ставка на 1/2 части стола\n"

        super().__init__(names, help_text, detail_help_text, conversation=True, int_args=[-1])

    def start(self):

        if self.vk_event.args:
            if len(Gamer.objects.filter(user=self.vk_event.sender)) == 0:
                Gamer(user=self.vk_event.sender).save()
            gamer = Gamer.objects.filter(user=self.vk_event.sender).first()

            self.args = 2
            self.check_args()

            rate_on = self.vk_event.args[0]
            rate = self.vk_event.args[-1]

            if rate >= gamer.roulette_points:
                return f"Ставка не может быть больше ваших очков - {gamer.roulette_points}"

            if rate_on in TRANSLATOR:
                if rate_on in ['строка', 'столбец']:
                    self.args = 3
                    self.int_args = [1, 2]
                    self.check_args()
                    self.parse_args('int')
                    rowcol = self.vk_event.args[1]
                    self.check_number_arg_range(rowcol, 1, 3)

                    rate_obj = TRANSLATOR[rate_on][rowcol]
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
