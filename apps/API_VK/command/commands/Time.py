import datetime

from apps.API_VK.APIs.world_time import get_time, get_timezones, check_city
from apps.API_VK.APIs.yandex_translate import get_translate
from apps.API_VK.command.CommonCommand import CommonCommand


# ToDo: создаём модель города, с полями [id,nameS,timezone,...]
# ToDo: не отправляем запрос, если город есть уже в списке
# ToDo: подумать, что делать с городами из других стран.
def parse_datetime(str_date):
    date_time_obj = datetime.datetime.strptime(str_date, "%Y-%m-%dT%H:%M:%S.%f%z")
    return date_time_obj.strftime("%d.%m.%Y\n%H:%M:%S")


class Time(CommonCommand):
    def __init__(self):
        names = ["время"]
        help_text = "Время - текущее время"
        detail_help_text = "Время [N] - текущее время в городе N, доступны Самара, Питер, Сызрань, Прибой. По умолчанию берёт город из профиля."
        super().__init__(names, help_text, detail_help_text)

    # ToDo: здесь таймзоны наверное, нужно будет убирать, либо подумать, что с ними делать
    def start(self):
        if self.vk_event.args is None:
            if self.vk_event.sender.city:
                city = self.vk_event.sender.city.capitalize()
            else:
                city = 'Самара'
        else:
            if self.vk_event.args[0].lower() == 'таймзоны':
                if len(self.vk_event.args) > 1:
                    arg = get_translate('ru-en', self.vk_event.args[1]).capitalize()
                else:
                    arg = "Europe"
                timezones = get_timezones(arg)
                timezones_str = "\n".join(timezones)
                return timezones_str

            else:
                city = self.vk_event.args[0].capitalize()
        city = check_city(city)
        if city:
            try:
                time = get_time(city)
            except:
                return "Ошибка"
            return parse_datetime(time)
        else:
            return "Я не знаю такого города пока что"
