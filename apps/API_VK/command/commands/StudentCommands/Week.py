import datetime

from apps.API_VK.command.CommonCommand import CommonCommand


class Week(CommonCommand):
    def __init__(self):
        names = ["неделя"]
        super().__init__(names)

    def start(self):
        self.vk_bot.send_message(self.vk_event.chat_id,
                                 str((datetime.datetime.now().isocalendar()[1] - 35)) + " неделя")
