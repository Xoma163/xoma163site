import datetime

from apps.API_VK.command.CommonCommand import CommonCommand


class TimeTable(CommonCommand):
    def __init__(self):
        names = ["расписание", "расп"]
        help_text = "̲Р̲а̲с̲п̲и̲с̲а̲н̲и̲е - картинка с расписанием"
        keyboard_student = {'text': 'Расписание', 'color': 'blue', 'row': 1, 'col': 1}
        super().__init__(names, help_text, for_student=True, keyboard_student=keyboard_student)

    def start(self):
        attachments = []
        photo = {'owner_id': -186416119, 'id': 457239626}
        attachments.append('photo{}_{}'.format(photo['owner_id'], photo['id']))
        return {'msg': str((datetime.datetime.now().isocalendar()[1] - 35)) + " неделя", 'attachments': attachments}
