from apps.API_VK.command.CommonCommand import CommonCommand


class Weather(CommonCommand):
    def __init__(self):
        names = ["погода"]
        super().__init__(names)

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

        self.vk_bot.send_message(self.vk_event.chat_id, weather)
