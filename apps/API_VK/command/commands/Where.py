import datetime

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.models import Log


class Where(CommonCommand):
    def __init__(self):
        names = ["где"]
        help_text = "̲Г̲д̲е - информация о чекточках"
        detail_help_text = "̲Г̲д̲е (N) - информация о чекточках, где N - имя, фамилия, логин/id, никнейм"
        super().__init__(names, help_text, detail_help_text, need_args=1)

    def start(self):

        try:
            user = self.vk_bot.get_user_by_name(self.vk_event.args)
        except RuntimeError as e:
            return str(e)

        today = datetime.datetime.now()
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
            msg = "%s\n%s" % (log.date.strftime("%H:%M:%S"), log.msg)
        return str(msg)
