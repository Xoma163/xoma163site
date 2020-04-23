from apps.API_VK.command.CommonCommand import CommonCommand
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
            if len(city) == 0:
                return "Не нашёл такой город. /город"
            city = city.first()
        else:
            city = self.vk_event.sender.city
            if not city:
                return "Не указан город в профиле. /город"

        if city.lat and city.lon:
            weather = get_weather(city)
        else:
            return "У города не указаны широта и долгота"

        return weather
