from apps.API_VK.command.CommonCommand import CommonCommand


class Diary(CommonCommand):
    def __init__(self):
        names = ["����������"]
        help_text = "���������� - ������ �� ����������"
        super().__init__(names, help_text)

    def start(self):
        return 'https://diary.xoma163.xyz/'