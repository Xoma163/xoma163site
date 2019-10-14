from django.core.management.base import BaseCommand

from xoma163site.settings import BASE_DIR


class Command(BaseCommand):
    # help = 'Displays current time'

    # python manage.py check_rasp
    def handle(self, *args, **kwargs):
        # неделя, день недели, время
        # schedule['1']['3']['1']
        schedule = {}
        schedule['1'] = {}
        schedule['1']['1'] = {}
        schedule['1']['1']['3'] = {}
        schedule['1']['1']['3']['TEACHER'] = "Прохоров С.А."
        schedule['1']['1']['3']['DISCIPLINE'] = "СПИВТ"
        schedule['1']['1']['3']['CABINET'] = "Логово"
        schedule['1']['1']['3']['TYPE'] = "🍎 Практика"
        schedule['1']['2'] = {}
        schedule['1']['2']['3'] = {}
        schedule['1']['2']['3']['TEACHER'] = "Прохоров С.А."
        schedule['1']['2']['3']['DISCIPLINE'] = "СПИВТ"
        schedule['1']['2']['3']['CABINET'] = "Логово"
        schedule['1']['2']['3']['TYPE'] = "🍋 Лаба"
        schedule['1']['2']['4'] = {}
        schedule['1']['2']['4']['TEACHER'] = "Прохоров С.А."
        schedule['1']['2']['4']['DISCIPLINE'] = "СПИВТ"
        schedule['1']['2']['4']['CABINET'] = "Логово"
        schedule['1']['2']['4']['TYPE'] = "🍋 Лаба"
        schedule['1']['3'] = {}
        schedule['1']['3']['2'] = {}
        schedule['1']['3']['2']['TEACHER'] = "Прохоров С.А."
        schedule['1']['3']['2']['DISCIPLINE'] = "СПИВТ"
        schedule['1']['3']['2']['CABINET'] = "430"
        schedule['1']['3']['2']['TYPE'] = "🍏 Лекция"
        schedule['1']['3']['3'] = {}
        schedule['1']['3']['3']['TEACHER'] = "Лёзина И.В."
        schedule['1']['3']['3']['DISCIPLINE'] = "ПРПО"
        schedule['1']['3']['3']['CABINET'] = "421"
        schedule['1']['3']['3']['TYPE'] = "🍎 Практика"
        schedule['1']['5'] = {}
        schedule['1']['5']['2'] = {}
        schedule['1']['5']['2']['TEACHER'] = "Лёзин И.А."
        schedule['1']['5']['2']['DISCIPLINE'] = "ТРПО"
        schedule['1']['5']['2']['CABINET'] = "505"
        schedule['1']['5']['2']['TYPE'] = "🍏 Лаба"
        schedule['2'] = {}
        schedule['2']['1'] = {}
        schedule['2']['1']['1'] = {}
        schedule['2']['1']['1']['TEACHER'] = "Лёзин И.А."
        schedule['2']['1']['1']['DISCIPLINE'] = "ТРПО"
        schedule['2']['1']['1']['CABINET'] = "510"
        schedule['2']['1']['1']['TYPE'] = "🍋 Лаба"
        schedule['2']['1']['2'] = {}
        schedule['2']['1']['2']['TEACHER'] = "Лёзин И.А."
        schedule['2']['1']['2']['DISCIPLINE'] = "ТРПО"
        schedule['2']['1']['2']['CABINET'] = "510"
        schedule['2']['1']['2']['TYPE'] = "🍋 Лаба"
        schedule['2']['3'] = {}
        schedule['2']['3']['5'] = {}
        schedule['2']['3']['5']['TEACHER'] = "Лёзина И.В."
        schedule['2']['3']['5']['DISCIPLINE'] = "ПРПО"
        schedule['2']['3']['5']['CABINET'] = "507"
        schedule['2']['3']['5']['TYPE'] = "🍋 Лаба"
        schedule['2']['3']['6'] = {}
        schedule['2']['3']['6']['TEACHER'] = "Лёзина И.В."
        schedule['2']['3']['6']['DISCIPLINE'] = "ПРПО"
        schedule['2']['3']['6']['CABINET'] = "507"
        schedule['2']['3']['6']['TYPE'] = "🍋 Лаба"
        schedule['2']['4'] = {}
        schedule['2']['4']['3'] = {}
        schedule['2']['4']['3']['TEACHER'] = "Прохоров С.А."
        schedule['2']['4']['3']['DISCIPLINE'] = "ПАСНИ"
        schedule['2']['4']['3']['CABINET'] = "Логово"
        schedule['2']['4']['3']['TYPE'] = "🍋 Лаба"
        schedule['2']['4']['4'] = {}
        schedule['2']['4']['4']['TEACHER'] = "Лёзина И.В."
        schedule['2']['4']['4']['DISCIPLINE'] = "ПРПО"
        schedule['2']['4']['4']['CABINET'] = "510"
        schedule['2']['4']['4']['TYPE'] = "🍎 Практика"
        schedule['2']['4']['4'] = {}
        schedule['2']['4']['4']['TEACHER'] = "Солдатова О.П."
        schedule['2']['4']['4']['DISCIPLINE'] = "ИС"
        schedule['2']['4']['4']['CABINET'] = "511"
        schedule['2']['4']['4']['TYPE'] = "🍋 Лаба"
        schedule['2']['4']['5'] = {}
        schedule['2']['4']['5']['TEACHER'] = "Солдатова О.П."
        schedule['2']['4']['5']['DISCIPLINE'] = "ИС"
        schedule['2']['4']['5']['CABINET'] = "511"
        schedule['2']['4']['5']['TYPE'] = "🍋 Лаба"
        schedule['2']['4']['6'] = {}
        schedule['2']['4']['6']['TEACHER'] = "Солдатова О.П."
        schedule['2']['4']['6']['DISCIPLINE'] = "ИС"
        schedule['2']['4']['6']['CABINET'] = "511"
        schedule['2']['4']['6']['TYPE'] = "🍋 Лаба"
        schedule['2']['5'] = {}
        schedule['2']['5']['5'] = {}
        schedule['2']['5']['5']['TEACHER'] = "Прохоров С.А."
        schedule['2']['5']['5']['DISCIPLINE'] = "ПАСНИ"
        schedule['2']['5']['5']['CABINET'] = "Логово"
        schedule['2']['5']['5']['TYPE'] = "🍋 Лаба"
        schedule['2']['5']['6'] = {}
        schedule['2']['5']['6']['TEACHER'] = "Прохоров С.А."
        schedule['2']['5']['6']['DISCIPLINE'] = "ПАСНИ"
        schedule['2']['5']['6']['CABINET'] = "Логово"
        schedule['2']['5']['6']['TYPE'] = "🍋 Лаба"
        print(schedule)

        with open(BASE_DIR + '/static/schedules/schedule.json', 'w') as outfile:
            import json
            json.dump(schedule, outfile)

        print('done')
