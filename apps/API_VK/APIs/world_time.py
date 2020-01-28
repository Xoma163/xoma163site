import requests


def check_city(city="Самара"):
    if city in ['Самара', 'Самаре', 'Смр', 'Сызрань', 'Сызрани', 'Прибой', 'Прибое']:
        return "Europe/Samara"
    elif city in ['Питер', 'Питере', 'Санкт-петербург', 'Санкт-петербурге', 'Спб', 'Купчино', 'Москва', 'Мск',
                  'Москве']:
        return "Europe/Moscow"
    else:
        return city


def get_time(city):
    URL = f"http://worldtimeapi.org/api/timezone/{city}"
    response = requests.get(URL).json()

    return response['datetime']


def get_timezones(continent="Europe"):
    URL = f"http://worldtimeapi.org/api/timezone/{continent}"
    response = requests.get(URL).json()
    return response
