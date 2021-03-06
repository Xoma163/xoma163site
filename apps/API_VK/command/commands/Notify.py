import json
from datetime import datetime, timedelta

import dateutil
from dateutil import parser

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import localize_datetime, normalize_datetime, remove_tz, check_user_group
from apps.API_VK.command.Consts import Role
from apps.API_VK.command.Consts import WEEK_TRANSLATOR
from apps.service.models import Notify as NotifyModel


# Возвращает datetime, кол-во аргументов использованных для получения даты, была ли передана точная дата и время
def get_time(arg1, arg2):
    exact_datetime_flag = True
    if arg1 == "завтра":
        exact_datetime_flag = False
        arg1 = (datetime.today().date() + timedelta(days=1)).strftime("%d.%m.%Y")
    if arg1 == "послезавтра":
        exact_datetime_flag = False
        arg1 = (datetime.today().date() + timedelta(days=2)).strftime("%d.%m.%Y")

    if arg1 in WEEK_TRANSLATOR:
        exact_datetime_flag = False
        delta_days = WEEK_TRANSLATOR[arg1] - datetime.today().isoweekday()
        if delta_days <= 0:
            delta_days += 7
        arg1 = (datetime.today().date() + timedelta(days=delta_days)).strftime("%d.%m.%Y")

    default_datetime = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)  # + timedelta(days=1)
    try:
        if arg1.count('.') == 1:
            arg1 = f"{arg1}.{default_datetime.year}"
        date_str = f"{arg1} {arg2}"

        return parser.parse(date_str, default=default_datetime, dayfirst=True), 2, exact_datetime_flag
    except dateutil.parser._parser.ParserError:
        try:
            exact_datetime_flag = False
            return parser.parse(arg1, default=default_datetime, dayfirst=True), 1, exact_datetime_flag
        except dateutil.parser._parser.ParserError:
            return None, None, None


class Notify(CommonCommand):
    def __init__(self):
        names = ["напомни", "напомнить", "оповещение", "оповести"]
        help_text = "Напомни - напоминает о чём-либо"
        detail_help_text = "Напомни (дата/дата и время/день недели) (сообщение/команда) [Прикреплённые вложения] - добавляет " \
                           "напоминание\n" \
                           "Максимум можно добавить 5 напоминаний"
        super().__init__(names, help_text, detail_help_text, args=2, api=False)

    def start(self):
        if self.vk_event.sender.city is None:
            return "Не знаю ваш город. /город"
        if not check_user_group(self.vk_event.sender, Role.TRUSTED) and \
                len(NotifyModel.objects.filter(author=self.vk_event.sender)) >= 5:
            return "Нельзя добавлять более 5 напоминаний"
        user_timezone = self.vk_event.sender.city.timezone.name

        date, args_count, exact_time_flag = get_time(self.vk_event.args[0], self.vk_event.args[1])
        if args_count == 2:
            self.check_args(3)
        if not date:
            return "Не смог распарсить дату"
        date = normalize_datetime(date, user_timezone)
        datetime_now = localize_datetime(datetime.utcnow(), "UTC")

        if (date - datetime_now).seconds < 60:
            return "Нельзя добавлять напоминание на ближайшую минуту"
        if not exact_time_flag and ((date - datetime_now).days < 0 or (datetime_now - date).seconds < 0):
            date = date + timedelta(days=1)
        if (date - datetime_now).days < 0 or (datetime_now - date).seconds < 0:
            return "Нельзя указывать дату в прошлом"

        text = self.vk_event.original_args.split(' ', args_count)[args_count]
        if text[0] == '/':
            first_space = text.find(' ')
            if first_space > 0:
                command = text[1:first_space]
            else:
                command = text[1:]
            from apps.API_VK.command.commands.NotifyRepeat import NotifyRepeat
            if command in self.names or command in NotifyRepeat().names:
                text = f"/обосрать {self.vk_event.sender.name}"
        notify_datetime = localize_datetime(remove_tz(date), user_timezone)

        notify = NotifyModel(date=date,
                             text=text,
                             author=self.vk_event.sender,
                             chat=self.vk_event.chat,
                             text_for_filter=notify_datetime.strftime("%d.%m.%Y %H:%M") + " " + text)
        if self.vk_event.attachments:
            notify.attachments = json.dumps(self.vk_event.attachments)
        notify.save()
        notify.text_for_filter += f" ({notify.id})"
        notify.save()

        return f'Сохранил на дату {str(notify_datetime.strftime("%d.%m.%Y %H:%M"))}'
