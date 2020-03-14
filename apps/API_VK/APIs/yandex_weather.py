from datetime import datetime

import requests

from apps.service.models import Service
from secrets.secrets import secrets


def get_weather(city):
    entity, created = Service.objects.get_or_create(name=f'weather_{city.name}')
    if not created:
        update_datetime = entity.update_datetime

        delta_seconds = (datetime.utcnow() - update_datetime.replace(tzinfo=None)).seconds
        if delta_seconds < 3600:
            return entity.value

    TOKEN = secrets['yandex']['weather']

    URL = f"https://api.weather.yandex.ru/v1/informers?lat={city.lat}&lon={city.lon}&lang=ru_RU"
    HEADERS = {'X-Yandex-API-Key': TOKEN}
    response = requests.get(URL, headers=HEADERS).json()
    if 'status' in response:
        if response['status'] == 403:
            return "На сегодня я исчерпал все запросы к Yandex Weather :("
    WEATHER_TRANSLATE = {
        'clear': 'Ясно ☀',
        'partly-cloudy': 'Малооблачно ⛅',
        'cloudy': 'Облачно с прояснениями 🌥',
        'overcast': 'Пасмурно ☁',
        'partly-cloudy-and-light-rain': 'Небольшой дождь 🌧',
        'partly-cloudy-and-rain': 'Дождь 🌧',
        'overcast-and-rain': 'Сильный дождь 🌧🌧',
        'overcast-thunderstorms-with-rain': 'Сильный дождь, гроза 🌩',
        'cloudy-and-light-rain': 'Небольшой дождь 🌧',
        'overcast-and-light-rain': 'Небольшой дождь 🌧',
        'cloudy-and-rain': 'Дождь 🌧',
        'overcast-and-wet-snow': 'Дождь со снегом 🌨',
        'partly-cloudy-and-light-snow': 'Небольшой снег 🌨',
        'partly-cloudy-and-snow': 'Снег 🌨',
        'overcast-and-snow': 'Снегопад 🌨',
        'cloudy-and-light-snow': 'Небольшой снег 🌨',
        'overcast-and-light-snow': 'Небольшой снег 🌨',
        'cloudy-and-snow': 'Снег 🌨'}
    DAY_TRANSLATE = {
        'night': 'ночь',
        'morning': 'утро',
        'day': 'день',
        'evening': 'вечер',
    }

    weather = {
        'now': {
            'temp': response['fact']['temp'],
            'temp_feels_like': response['fact']['feels_like'],
            'condition': WEATHER_TRANSLATE[response['fact']['condition']],
            'wind_speed': response['fact']['wind_speed'],
            'wind_gust': response['fact']['wind_gust'],
            'pressure': response['fact']['pressure_mm'],
            'humidity': response['fact']['humidity'],
        },
        'forecast': {}}

    for i in range(len(response['forecast']['parts'])):
        weather['forecast'][i] = {
            'part_name': DAY_TRANSLATE[response['forecast']['parts'][i]['part_name']],
            'temp_min': response['forecast']['parts'][i]['temp_min'],
            'temp_max': response['forecast']['parts'][i]['temp_max'],
            'temp_feels_like': response['forecast']['parts'][i]['feels_like'],
            'condition': WEATHER_TRANSLATE[response['forecast']['parts'][i]['condition']],
            'wind_speed': response['forecast']['parts'][i]['wind_speed'],
            'wind_gust': response['forecast']['parts'][i]['wind_gust'],
            'pressure': response['forecast']['parts'][i]['pressure_mm'],
            'humidity': response['forecast']['parts'][i]['humidity'],
            'prec_mm': response['forecast']['parts'][i]['prec_mm'],
            'prec_period': int(int(response['forecast']['parts'][i]['prec_period']) / 60),
            'prec_prob': response['forecast']['parts'][i]['prec_prob'],
        }

    now = f"Погода в городе {city.name} сейчас:\n" \
          f"{weather['now']['condition']}\n" \
          f"Температура {weather['now']['temp']}°С(ощущается как {weather['now']['temp_feels_like']}°С)\n" \
          f"Ветер {weather['now']['wind_speed']}м/c(порывы до {weather['now']['wind_gust']}м/c)\n" \
          f"Давление  {weather['now']['pressure']}мм.рт.ст., влажность {weather['now']['humidity']}%"

    forecast = ""
    for i in range(len(weather['forecast'])):
        forecast += f"\n\n" \
            f"Прогноз на {weather['forecast'][i]['part_name']}:\n" \
            f"{weather['forecast'][i]['condition']}\n"

        if weather['forecast'][i]['temp_min'] != weather['forecast'][i]['temp_max']:
            forecast += f"Температура от {weather['forecast'][i]['temp_min']} до {weather['forecast'][i]['temp_max']}°С"
        else:
            forecast += f"Температура {weather['forecast'][i]['temp_max']}°С"

        forecast += f"(ощущается как {weather['forecast'][i]['temp_feels_like']}°С)\n" \
            f"Ветер {weather['forecast'][i]['wind_speed']}м/c(порывы до {weather['forecast'][i]['wind_gust']}м/c)\n" \
            f"Давление {weather['forecast'][i]['pressure']} мм.рт.ст., влажность {weather['forecast'][i]['humidity']}%\n"
        if weather['forecast'][i]['prec_mm'] != 0:
            forecast += f"Осадки {weather['forecast'][i]['prec_mm']}мм " \
                f"на протяжении {weather['forecast'][i]['prec_period']} часов " \
                f"с вероятностью {weather['forecast'][i]['prec_prob']}%"
        else:
            forecast += "Без осадков"
    entity.value = now + forecast
    entity.save()
    return entity.value
