from apps.API_VK.command.CommonCommand import CommonCommand


class GoogleDrive(CommonCommand):
    def __init__(self):
        names = ["гугл", "ссылка", "учебное"]
        help_text = "̲У̲ч̲е̲б̲н̲о̲е - ссылка на папку с учебным материалом"
        keyboard_student = {'text': 'Учебное', 'color': 'blue', 'row': 1, 'col': 3}
        super().__init__(names, help_text, for_student=True, keyboard_student=keyboard_student)

    def start(self):
        return "https://drive.google.com/open?id=1AJPnT2XXYNc39-2CSr_MzHnv4hs6Use6"
