import datetime

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import localize_datetime, remove_tz
from apps.API_VK.models import Log
from xoma163site.settings import TIME_ZONE


class Where(CommonCommand):
    def __init__(self):
        names = ["где"]
        help_text = "Где - информация о чекточках"
        detail_help_text = "Где (N) - информация о чекточках, где N - имя, фамилия, логин/id, никнейм"
        super().__init__(names, help_text, detail_help_text, args=1, access='trusted')

    def start(self):

        try:
            user = self.vk_bot.get_user_by_name(self.vk_event.args, self.vk_event.chat)
        except RuntimeError as e:
            return str(e)

        if self.vk_event.sender.city and self.vk_event.sender.city.timezone:
            timezone = self.vk_event.sender.city.timezone
        else:
            timezone = TIME_ZONE
        today = localize_datetime(datetime.datetime.utcnow(), timezone)
        log = Log.objects.filter(success=True,
                                 date__year=today.year,
                                 date__month=today.month,
                                 date__day=today.day,
                                 author=user).first()
        if user is None:
            msg = "Такого пользователя нет"
        elif log is None:
            msg = "Информации пока ещё нет"
        else:
            localized_date = localize_datetime(remove_tz(log.date), timezone)
            msg = "%s\n%s" % (localized_date.strftime("%H:%M:%S"), log.msg)
        return str(msg)
