from datetime import datetime

import requests

from apps.Statistics.models import Service
from secrets.secrets import secrets


def get_time(city="Самара"):
    if city in ['Самара', 'Самаре', 'Смр', 'Сызрань', 'Сызрани', 'Прибой', 'Прибое']:
        original_city_name = "Europe/Samara"
    elif city in ['Питер', 'Питере', 'Санкт-петербург', 'Санкт-петербурге', 'Спб', 'Купчино', 'Москва', 'Мск', 'Москве']:
        original_city_name = "Europe/Moscow"

    URL = f"http://worldtimeapi.org/api/timezone/%{original_city_name}"
    response = requests.get(URL, headers=HEADERS).json()

    return response.datetime


def get_timezones(continent="Europe"):
    URL = f"http://worldtimeapi.org/api/timezone/%{continent}"
    response = requests.get(URL, headers=HEADERS).json()
    return response
