from apps.API_VK.command.CommonCommand import CommonCommand


class GoogleDrive(CommonCommand):
    def __init__(self):
        names = ["гугл", "ссылка", "учебное"]
        super().__init__(names, for_student=True)

    def start(self):
        self.vk_bot.send_message(self.vk_event.chat_id,
                                 "https://drive.google.com/open?id=1AJPnT2XXYNc39-2CSr_MzHnv4hs6Use6")
