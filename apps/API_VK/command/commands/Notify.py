from datetime import datetime, timedelta

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import localize_datetime, normalize_datetime, remove_tz
from apps.service.models import Notify as NotifyModel

time_translator = {
    'понедельник': 1, 'пн': 1,
    'вторник': 2, 'вт': 2,
    'среда': 3, 'ср': 3,
    'четверг': 4, 'чт': 4,
    'пятница': 5, 'пт': 5,
    'суббота': 6, 'сб': 6,
    'воскресенье': 7, 'воскресение': 7, 'вс': 7,
}


def get_time(arg1, arg2):
    if arg1 == "завтра":
        arg1 = (datetime.today().date() + timedelta(days=1)).strftime("%d.%m.%Y")
    if arg1 == "послезавтра":
        arg1 = (datetime.today().date() + timedelta(days=2)).strftime("%d.%m.%Y")

    if arg1 in time_translator:
        delta_days = time_translator[arg1] - datetime.today().isoweekday()
        if delta_days < 0:
            delta_days += 7
        arg1 = (datetime.today().date() + timedelta(days=delta_days)).strftime("%d.%m.%Y")
    try:
        date = datetime.strptime(str(datetime.today().date()) + " " + arg1, "%Y-%m-%d %H:%M")
        return date, 1
    except:
        try:
            date = datetime.strptime(arg1 + " " + arg2, "%d.%m.%Y %H:%M")
            return date, 2
        except:
            try:
                date = datetime.strptime(arg1 + " 10:00", "%d.%m.%Y %H:%M")
                return date, 1
            except:
                pass
    return None, None


class Notify(CommonCommand):
    def __init__(self):
        names = ["напомни", "напомнить", "напоминания", "оповещение", "оповещения", "оповести"]
        help_text = "Напомни - напоминает о чём-либо"
        detail_help_text = "Напомни (N,M) - добавляет напоминание. N = Дата(полная в формате %d.%m.%Y %H:%M или %H:%M), M - сообщение"
        super().__init__(names, help_text, detail_help_text, args=2)

    def start(self):
        if self.vk_event.sender.city is None:
            return "Не знаю ваш город. /город"
        user_timezone = self.vk_event.sender.city.timezone

        date, args_count = get_time(self.vk_event.args[0], self.vk_event.args[1])
        if not date:
            return "Не смог распарсить дату"
        date = normalize_datetime(date, user_timezone)
        datetime_now = localize_datetime(datetime.utcnow(), "UTC")
        if (date - datetime_now).days < 0 or (datetime_now - date).seconds < 0:
            return "Нельзя указывать дату в прошлом"
        if (date - datetime_now).seconds < 60:
            return "Нельзя добавлять напоминание на ближайшую минуту"
        text = self.vk_event.original_args.split(' ', args_count)[args_count]

        NotifyModel(date=date,
                    text=text,
                    author=self.vk_event.sender,
                    chat=self.vk_event.chat,
                    from_chat=self.vk_event.from_chat).save()

        notify_datetime = localize_datetime(remove_tz(date), user_timezone)
        return f'Сохранил на дату {str(notify_datetime.strftime("%d.%m.%Y %H:%M"))}'
