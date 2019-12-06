from apps.API_VK.command.CommonCommand import CommonCommand, check_sender_admin
from apps.Statistics.models import Service


class Stream(CommonCommand):
    def __init__(self):
        names = ["стрим", "поток"]
        help_text = "̲С̲т̲р̲и̲м - ссылка на стрим"
        super().__init__(names, help_text)

    def start(self):
        if self.vk_event.args is None:
            stream, created = Service.objects.get_or_create(name="stream")
            stream_link = stream.value
            if len(stream_link) < 5:
                self.vk_bot.send_message(self.vk_event.chat_id, "Стрим пока не идёт")
                return
            else:
                self.vk_bot.send_message(self.vk_event.chat_id, stream_link)
        else:
            if not check_sender_admin(self.vk_bot, self.vk_event):
                return
            Service.objects.update_or_create(name="stream", defaults={'value': self.vk_event.args[0]})
            self.vk_bot.send_message(self.vk_event.chat_id, "Ссылка изменена на " + self.vk_event.args[0])
