import json
from datetime import datetime

import requests

from apps.API_VK.command.CommonMethods import remove_tz
from apps.API_VK.command.Consts import DAY_TRANSLATE
from apps.service.models import Service
from secrets.secrets import secrets


class YandexWeatherAPI:
    def __init__(self, city):
        self.url = "https://api.weather.yandex.ru/v1/informers"
        self.city = city

    def send_weather_request(self):
        TOKEN = secrets['yandex']['weather']

        params = {
            'lat': self.city.lat,
            'lon': self.city.lon,
            'lang': 'ru_RU'
        }
        HEADERS = {'X-Yandex-API-Key': TOKEN}
        response = requests.get(self.url, params, headers=HEADERS).json()
        if 'status' in response:
            if response['status'] == 403:
                return "На сегодня я исчерпал все запросы к Yandex Weather :("

        fact = response['fact']
        weather = {
            'now': {
                'temp': fact['temp'],
                'temp_feels_like': fact['feels_like'],
                'condition': fact['condition'],
                'wind_speed': fact['wind_speed'],
                'wind_gust': fact['wind_gust'],
                'pressure': fact['pressure_mm'],
                'humidity': fact['humidity'],
            },
            'forecast': []}

        # Проставление part_name для времени сейчас
        index = list(DAY_TRANSLATE.keys()).index(response['forecast']['parts'][0]['part_name'])
        weather['now']['part_name'] = list(DAY_TRANSLATE.keys())[index - 1]

        for x in response['forecast']['parts']:
            weather['forecast'].append({
                'part_name': x['part_name'],
                'temp_min': x['temp_min'],
                'temp_max': x['temp_max'],
                'temp_feels_like': x['feels_like'],
                'condition': x['condition'],
                'wind_speed': x['wind_speed'],
                'wind_gust': x['wind_gust'],
                'pressure': x['pressure_mm'],
                'humidity': x['humidity'],
                'prec_mm': x['prec_mm'],
                'prec_period': int(int(x['prec_period']) / 60),
                'prec_prob': x['prec_prob'],
            })
        return weather

    def get_weather(self, use_cached=True):
        entity, created = Service.objects.get_or_create(name=f'weather_{self.city.name}')
        if use_cached and not created:
            delta_time = (datetime.utcnow() - remove_tz(entity.update_datetime))
            if delta_time.seconds < 3600 and delta_time.days == 0:
                weather_data = json.loads(entity.value)
                return weather_data

        weather_data = self.send_weather_request()
        entity.value = json.dumps(weather_data)
        entity.save()
        return weather_data
