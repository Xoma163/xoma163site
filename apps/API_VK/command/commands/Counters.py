from apps.API_VK.command.CommonCommand import CommonCommand
from apps.service.models import Counter as CounterModel


class Counters(CommonCommand):
    def __init__(self):
        names = ["счётчики", "счетчики"]
        help_text = "Счётчики - список счётчиков"
        super().__init__(names, help_text)

    def start(self):
        counters = CounterModel.objects.filter(chat=self.vk_event.chat).order_by('-count').values()
        msg = "Счётчики:\n"
        for counter in counters:
            msg += f"{counter['name']} - {counter['count']}\n"
        return msg
