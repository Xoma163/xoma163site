from datetime import datetime, timedelta

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import localize_datetime, normalize_datetime, remove_tz
from apps.service.models import Notify as NotifyModel


def get_time(time):
    try:
        date = datetime.strptime(str(datetime.today().date()) + " " + time, "%Y-%m-%d %H:%M")
        return date
    except Exception as e:
        print(e)
        return None


class NotifyRepeat(CommonCommand):
    def __init__(self):
        names = ["напоминай", "оповещай"]
        help_text = "Напоминай - напоминает о чём-либо постояно"
        detail_help_text = "Напомни ({время}, {сообщение}) - добавляет напоминание на постоянной основе."
        super().__init__(names, help_text, detail_help_text, args=2)

    def start(self):
        if self.vk_event.sender.city is None:
            return "Не знаю ваш город. /город"
        user_timezone = self.vk_event.sender.city.timezone

        date = get_time(self.vk_event.args[0])
        if not date:
            return "Не смог распарсить дату"
        date = normalize_datetime(date, user_timezone)
        datetime_now = localize_datetime(datetime.utcnow(), "UTC")

        if (date - datetime_now).seconds < 60:
            return "Нельзя добавлять напоминание на ближайшую минуту"

        if (date - datetime_now).days < 0 or (datetime_now - date).seconds < 0:
            date = date + timedelta(days=1)

        text = self.vk_event.original_args.split(' ', 1)[1]
        if text[0] == '/':
            first_space = text.find(' ')
            if first_space > 0:
                command = text[1:first_space]
            else:
                command = text[1:]
            from apps.API_VK.command.commands.Notify import Notify
            if command in self.names or command in Notify().names:
                text = f"/обосрать {self.vk_event.sender.name}"
        notify_datetime = localize_datetime(remove_tz(date), user_timezone)

        NotifyModel(date=date,
                    text=text,
                    author=self.vk_event.sender,
                    chat=self.vk_event.chat,
                    from_chat=self.vk_event.from_chat,
                    repeat=True,
                    text_for_filter=notify_datetime.strftime("%H:%M") + " " + text).save()

        return f'Следующее выполнение - {str(notify_datetime.strftime("%d.%m.%Y %H:%M"))}'
