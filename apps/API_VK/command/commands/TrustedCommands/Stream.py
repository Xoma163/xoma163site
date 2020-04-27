from apps.API_VK.command.CommonCommand import CommonCommand
from apps.service.models import Service


class Stream(CommonCommand):
    def __init__(self):
        names = ["стрим", "поток"]
        help_text = "Стрим - ссылка на стрим"
        detail_help_text = "Стрим - ссылка на стрим\n" \
                           "Стрим [новая ссылка] - меняет ссылку на стрим. Требуются права модератора"
        super().__init__(names, help_text, detail_help_text, access='trusted')

    def start(self):
        if self.vk_event.args is None:
            stream, _ = Service.objects.get_or_create(name="stream")
            stream_link = stream.value
            if len(stream_link) < 5:
                return "Стрим пока не идёт"
            else:
                return stream_link
        else:
            self.check_sender(['trusted', 'moderator'])
            Service.objects.update_or_create(name="stream", defaults={'value': self.vk_event.args[0]})
            return "Ссылка изменена на " + self.vk_event.args[0]