from apps.API_VK.command.CommonCommand import CommonCommand
from apps.Statistics.models import Counter as CounterModel


class Counter(CommonCommand):
    def __init__(self):
        names = ["счётчик", "счетчик", "счёт", "счет"]
        help_text = "Счётчик - счётчик события"
        detail_help_text = "Счётчик (N) - счётчик события N. Инкремент"
        super().__init__(names, help_text, detail_help_text, need_args=1)

    def start(self):
        name = self.vk_event.original_args.capitalize()
        if len(name) >= 50:
            return "Длина названия счётчика не может превышать 50"

        counter, created = CounterModel.objects.update_or_create(name=name, chat=self.vk_event.chat,
                                                                 defaults={
                                                                     'name': name,
                                                                     'chat': self.vk_event.chat
                                                                 })
        counter.count += 1
        counter.save()
        return "++"
