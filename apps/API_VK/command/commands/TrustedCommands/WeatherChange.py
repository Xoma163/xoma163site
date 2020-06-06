import json

from apps.API_VK.APIs.YandexWeatherAPI import YandexWeatherAPI
from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.Consts import Role, WEATHER_TRANSLATE
from apps.service.models import Service, City


class WeatherChange(CommonCommand):
    def __init__(self):
        names = ["погодаизм", "измпогоды", 'измпогода']
        help_text = "Погодаизм - присылает изменения погоды по сравнению со вчерашним днём"
        detail_help_text = "Погодаизм [город=из профиля] - присылает изменения погоды по сравнению со вчерашним днём\n" \
                           "Обновление погоды происходит в 12 дня"
        super().__init__(names, help_text, detail_help_text, access=Role.TRUSTED)

    def start(self):

        if self.vk_event.args:
            city = City.objects.filter(name__icontains=" ".join(self.vk_event.args))
            if not city:
                return "Не нашёл такого города"
        else:
            city = self.vk_event.sender.city
            if not city:
                return "Не указан город в профиле"

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
            difference += f"Ощущаемая температура {delta_feels_temp} градусов больше, чем вчера\n"
        elif delta_feels_temp <= -5:
            difference += f"Ощущаемая температура {-delta_feels_temp} градусов больше, чем вчера\n"

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
