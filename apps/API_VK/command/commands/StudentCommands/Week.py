import datetime

from apps.API_VK.command.CommonCommand import CommonCommand


class Week(CommonCommand):
    def __init__(self):
        names = ["неделя"]
        help_text = "̲Н̲е̲д̲е̲л̲я - номер текущей учебной недели"
        super().__init__(names, help_text, for_student=True)

    def start(self):
        return str((datetime.datetime.now().isocalendar()[1] - 35)) + " неделя"
