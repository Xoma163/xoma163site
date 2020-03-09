from datetime import datetime

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.service.models import Notify as NotifyModel


def get_time(arg1, arg2):
    try:
        date = datetime.strptime(str(datetime.today().date()) + " " + arg1, "%Y-%m-%d %H:%M")
        return 1, date
    except:
        try:
            date = datetime.strptime(arg1 + " " + arg2, "%d.%m.%Y %H:%M")
            return 2, date
        except:
            pass
    return None


class Notify(CommonCommand):
    def __init__(self):
        names = ["напомни", "напомнить", "напоминания", "оповещение", "оповещения", "оповести"]
        help_text = "Напомни - напоминает о чём-либо"
        detail_help_text = "Напомни (N,M) - добавляет напоминание. N = Дата(полная в формате %d.%m.%Y %H:%M или %H:%M), M - сообщение"
        super().__init__(names, help_text, detail_help_text, args=2)

    def start(self):
        args_count, date = get_time(self.vk_event.args[0], self.vk_event.args[1])
        if not date:
            return "Не смог распарсить дату"
        if (date - datetime.now()).days < 0 or (datetime.now() - date).seconds < 0:
            return "Нельзя указывать дату в прошлом"
        text = self.vk_event.original_args.split(' ', args_count)[args_count]

        NotifyModel(date=date,
                    text=text,
                    author=self.vk_event.sender,
                    chat=self.vk_event.chat,
                    from_chat=self.vk_event.from_chat).save()

        return f'Сохранил на дату {str(date.strftime("%d.%m.%Y %H:%M"))}'
