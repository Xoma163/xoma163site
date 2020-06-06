import json

from apps.API_VK.APIs.YandexWeatherAPI import YandexWeatherAPI
from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.Consts import WEATHER_TRANSLATE, DAY_TRANSLATE
from apps.service.models import City, Service


class Weather(CommonCommand):
    def __init__(self):
        names = ["погода"]
        help_text = "Погода - прогноз погоды"
        detail_help_text = "Погода [город=из профиля] - прогноз погоды\n" \
                           "Погода [город=из профиля] изм/изменения - изменения погоды по сравнению со вчерашним днём. " \
                           "Работает не для всех городов"
        keyboard = {'text': 'Погода', 'color': 'blue', 'row': 1, 'col': 1}
        super().__init__(names, help_text, detail_help_text, keyboard=keyboard)

    def start(self):
        changes = False
        if self.vk_event.args and self.vk_event.args[-1].find("изм") >= 0:
            changes = True
            del self.vk_event.args[-1]
        if self.vk_event.args:
            city = City.objects.filter(synonyms__icontains=self.vk_event.args[0])
            if not city.exists():
                return "Не нашёл такой город. /город"
            city = city.first()
        else:
            city = self.vk_event.sender.city
            if not city:
                return "Не указан город в профиле. /город"
        if not (city.lat and city.lon):
            return "У города не указаны широта и долгота"

        # Изменения погоды теперь слиты в одну команду с погодой
        if changes:
            return self.weather_changes(city)
        yandexweather_api = YandexWeatherAPI(city)
        weather_data = yandexweather_api.get_weather()
        weather_str = get_weather_str(city, weather_data)
        return weather_str

    def weather_changes(self, city):
        entity_yesterday = Service.objects.filter(name=f'weatherchange_yesterday_{city.name}')
        if not entity_yesterday.exists():
            return "Не нашёл вчерашней погоды для этого города."
        weather_yesterday = json.loads(entity_yesterday.first().value)
        yandexweather_api = YandexWeatherAPI(city)
        weather_today = yandexweather_api.get_weather()

        part_yesterday = self.get_part(weather_yesterday)
        part_today = self.get_part(weather_today)

        difference = ""

        # Если погода не ясная или не облачная
        clear_weather_statuses = ['clear', 'partly-cloudy', 'cloudy', 'overcast']
        if part_today['condition'] not in clear_weather_statuses:
            weather_today_str = WEATHER_TRANSLATE[part_today['condition']].lower()
            difference += f"Ожидается {weather_today_str}\n"

        avg_temp_yesterday = self.get_avg_temp(part_yesterday)
        avg_temp_today = self.get_avg_temp(part_today)

        # Изменение температуры на 5 градусов
        delta_temp = avg_temp_yesterday - avg_temp_today
        if delta_temp >= 5:
            difference += f"Температура на {delta_temp} градусов больше, чем вчера\n"
        elif delta_temp <= -5:
            difference += f"Температура на {-delta_temp} градусов меньше, чем вчера\n"

        # Разница ощущаемой и по факту температур
        delta_feels_temp = avg_temp_today - part_today['temp_feels_like']
        if delta_feels_temp >= 5:
            difference += f"Ощущаемая температура на {delta_feels_temp} градусов больше, чем вчера\n"
        elif delta_feels_temp <= -5:
            difference += f"Ощущаемая температура на {-delta_feels_temp} градусов больше, чем вчера\n"

        # Скорость ветра
        if part_today['wind_speed'] > 10:
            difference += f"Скорость ветра {part_today['wind_speed']}м/с\n"
        if part_today['wind_gust'] > 10:
            difference += f"Порывы скорости ветра до {part_today['wind_gust']}м/с\n"

        if not difference:
            return "Нет изменений в погоде"
        return difference

    @staticmethod
    def get_part(weather):
        def get_part_for(_type='day'):
            if weather['now']['part_name'] == _type:
                return weather['now']
            elif weather['forecast'][0]['part_name'] == _type:
                return weather['forecast'][0]
            elif weather['forecast'][1]['part_name'] == _type:
                return weather['forecast'][1]
            return None

        part = get_part_for('day') or get_part_for('evening')
        if not part:
            raise RuntimeWarning('Сейчас у меня нет информации о погоде на день/вечер')
        return part

    @staticmethod
    def get_avg_temp(weather):
        if 'temp' in weather:
            return weather['temp']
        elif 'temp_min' in weather:
            return (weather['temp_max'] + weather['temp_min']) / 2


def get_weather_str(city, weather_data):
    now = \
        f"Погода в городе {city.name} сейчас:\n" \
        f"{WEATHER_TRANSLATE[weather_data['now']['condition']]}\n" \
        f"Температура {weather_data['now']['temp']}°С(ощущается как {weather_data['now']['temp_feels_like']}°С)\n" \
        f"Ветер {weather_data['now']['wind_speed']}м/c(порывы до {weather_data['now']['wind_gust']}м/c)\n" \
        f"Давление {weather_data['now']['pressure']}мм.рт.ст., влажность {weather_data['now']['humidity']}%"

    forecast = ""
    for x in weather_data['forecast']:
        forecast += \
            f"\n\n" \
            f"Прогноз на {DAY_TRANSLATE[x['part_name']]}:\n" \
            f"{WEATHER_TRANSLATE[x['condition']]}\n"

        if x['temp_min'] != x['temp_max']:
            forecast += f"Температура от {x['temp_min']} до {x['temp_max']}°С"
        else:
            forecast += f"Температура {x['temp_max']}°С"

        forecast += \
            f"(ощущается как {x['temp_feels_like']}°С)\n" \
            f"Ветер {x['wind_speed']}м/c(порывы до {x['wind_gust']}м/c)\n" \
            f"Давление {x['pressure']} мм.рт.ст., влажность {x['humidity']}%\n"
        if x['prec_mm'] != 0:
            forecast += \
                f"Осадки {x['prec_mm']}мм " \
                f"на протяжении {x['prec_period']} часов " \
                f"с вероятностью {x['prec_prob']}%"
        else:
            forecast += "Без осадков"
    return now + forecast
