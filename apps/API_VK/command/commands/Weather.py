from apps.API_VK.command.CommonCommand import CommonCommand


class Weather(CommonCommand):
    def __init__(self):
        names = ["погода"]
        help_text = "̲П̲о̲г̲о̲д̲а - прогноз погоды"
        detail_help_text = "Погода [N] - прогноз погоды в городе N, доступны Самара, Питер, Сызрань, Прибой. По умолчанию берёт город из профиля"
        keyboard = {'text': 'Погода', 'color': 'blue', 'row': 1, 'col': 1}
        super().__init__(names, help_text, detail_help_text, keyboard=keyboard)

    def start(self):
        if self.vk_event.args is None:
            if self.vk_event.sender.city:
                city = self.vk_event.sender.city.capitalize()
            else:
                city = 'Самара'
        else:
            city = self.vk_event.args[0].capitalize()
        from apps.API_VK.APIs.yandex_weather import get_weather

        weather = get_weather(city)

        return weather
