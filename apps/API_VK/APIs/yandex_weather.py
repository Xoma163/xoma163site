from datetime import datetime

import requests

from apps.Statistics.models import Service
from secrets.secrets import secrets


def get_weather(city="самара"):
    if city in ["Самара", "Самаре"]:
        original_city_name = "Самара"
        city_name = "Самаре"
        lat = 53.212273
        lon = 50.169435
    elif city in ['Питер', 'Питере', 'Санкт-петербург', 'Санкт-петербурге', 'Спб']:
        original_city_name = "Питер"
        city_name = "Питере"
        lat = 59.939095
        lon = 30.315868
    elif city in ['Сызрань', 'Сызрани']:
        original_city_name = "Сызрань"
        city_name = "Сызрани"
        lat = 53.155782
        lon = 48.474485
    elif city in ['Прибой', 'Прибое']:
        original_city_name = "Прибой"
        city_name = "Прибое"
        lat = 52.8689435
        lon = 49.6516931
    elif city in ['Купчино']:
        original_city_name = "Купчино"
        city_name = "Купчино"
        lat = 59.872380
        lon = 30.370291
    else:
        return 'Я не знаю координат города {}. Сообщите их разработчику'.format(city)

    entity, created = Service.objects.get_or_create(name='weather_{}'.format(original_city_name))
    if not created:
        update_datetime = entity.update_datetime
        delta_seconds = (datetime.now() - update_datetime).seconds
        if delta_seconds < 3600:
            return entity.value

    TOKEN = secrets['yandex']['weather']

    URL = "https://api.weather.yandex.ru/v1/informers?lat={}&lon={}&lang=ru_RU".format(lat, lon)
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

    now = 'Погода в {} сейчас:\n' \
          '{}\n' \
          'Температура {}°С(ощущается как {}°С)\n' \
          'Ветер {}м/c(порывы до {}м/c)\n' \
          'Давление  {}мм.рт.ст., влажность {}%'.format(city_name,
                                                        weather['now']['condition'], weather['now']['temp'],
                                                        weather['now']['temp_feels_like'],
                                                        weather['now']['wind_speed'], weather['now']['wind_gust'],
                                                        weather['now']['pressure'],
                                                        weather['now']['humidity'])

    forecast = ""
    for i in range(len(weather['forecast'])):
        forecast += '\n\n' \
                    'Прогноз на {}:\n' \
                    '{}\n'.format(
            weather['forecast'][i]['part_name'],
            weather['forecast'][i]['condition'])

        if weather['forecast'][i]['temp_min'] != weather['forecast'][i]['temp_max']:
            forecast += 'Температура от {} до {}°С'.format(weather['forecast'][i]['temp_min'],
                                                           weather['forecast'][i]['temp_max'])
        else:
            forecast += 'Температура {}°С'.format(weather['forecast'][i]['temp_max'])

        forecast += '(ощущается как {}°С)\n' \
                    'Ветер {}м/c(порывы до {}м/c)\n' \
                    'Давление {} мм.рт.ст., влажность {}%\n'.format(weather['forecast'][i]['temp_feels_like'],
                                                                    weather['forecast'][i]['wind_speed'],
                                                                    weather['forecast'][i]['wind_gust'],
                                                                    weather['forecast'][i]['pressure'],
                                                                    weather['forecast'][i]['humidity']
                                                                    )
        if weather['forecast'][i]['prec_mm'] != 0:
            forecast += 'Осадки {}мм на протяжении {} часов с вероятностью {}%'.format(
                weather['forecast'][i]['prec_mm'],
                weather['forecast'][i]['prec_period'],
                weather['forecast'][i]['prec_prob'])
        else:
            forecast += "Без осадков"
    entity.value = now + forecast
    entity.save()
    return entity.value
