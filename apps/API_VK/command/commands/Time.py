import datetime

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import localize_datetime
from apps.service.models import City


class Time(CommonCommand):
    def __init__(self):
        names = ["время"]
        help_text = "Время - текущее время"
        detail_help_text = "Время [N] - текущее время в городе"
        super().__init__(names, help_text, detail_help_text)

    def start(self):
        if self.vk_event.args:
            city = City.objects.filter(synonyms__icontains=self.vk_event.args[0]).first()
        else:
            city = self.vk_event.sender.city
        if not city:
            return "Город не найден. /город добавить"
        if not city.timezone:
            return "Таймзона у города не найдена"

        new_date = localize_datetime(datetime.datetime.utcnow(), city.timezone)
        return new_date.strftime("%d.%m.%Y\n%H:%M:%S")
