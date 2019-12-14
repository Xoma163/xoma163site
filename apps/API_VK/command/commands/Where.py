import datetime

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.models import Log


class Where(CommonCommand):
    def __init__(self):
        names = ["где"]
        help_text = "̲Г̲д̲е N(N - имя человека) - информация о чекточках"
        super().__init__(names, help_text, check_args=1)

    def start(self):

        try:
            user = self.vk_bot.get_user_by_name(self.vk_event.args)
        except RuntimeError as e:
            self.vk_bot.send_message(self.vk_event.chat_id, str(e))
            return

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
        self.vk_bot.send_message(self.vk_event.chat_id, str(msg))
