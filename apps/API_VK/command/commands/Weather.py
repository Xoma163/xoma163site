from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.Consts import WEATHER_TRANSLATE, DAY_TRANSLATE
from apps.service.models import City


class Weather(CommonCommand):
    def __init__(self):
        names = ["погода"]
        help_text = "Погода - прогноз погоды"
        detail_help_text = "Погода [город=из профиля] - прогноз погоды"
        keyboard = {'text': 'Погода', 'color': 'blue', 'row': 1, 'col': 1}
        super().__init__(names, help_text, detail_help_text, keyboard=keyboard)

    def start(self):
        from apps.API_VK.APIs.yandex_weather import get_weather

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

        weather_data = get_weather(city)
        weather_str = get_weather_str(city, weather_data)
        return weather_str


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
