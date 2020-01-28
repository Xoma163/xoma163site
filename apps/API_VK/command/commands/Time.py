from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.APIs.world_time import get_time, get_timezones

class Time(CommonCommand):
    def __init__(self):
        names = ["время"]
        help_text = "̲Время - текущее время"
        detail_help_text = "Время [N] - текущее время в городе N, доступны Самара, Питер, Сызрань, Прибой. По умолчанию берёт город из профиля."
        super().__init__(names, help_text, detail_help_text, keyboard=keyboard)

    def start(self):
        if self.vk_event.args is None:
            if self.vk_event.sender.city:
                city = self.vk_event.sender.city.capitalize()
            else:
                city = 'Самара'
        else:
            if self.vk_event.args[0] == 'таймзоны':
                return get_timezones(self.vk_event.args[1])
            else:
                city = self.vk_event.args[0].capitalize()
        time = get_time(city)
        return time
