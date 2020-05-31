from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.Consts import Role
from apps.service.models import Service


class Stream(CommonCommand):
    def __init__(self):
        names = ["стрим", "поток"]
        help_text = "Стрим - ссылка на стрим"
        detail_help_text = "Стрим - ссылка на стрим\n" \
                           "Стрим [новая ссылка] - меняет ссылку на стрим. Требуются права модератора"
        super().__init__(names, help_text, detail_help_text, access=Role.TRUSTED)

    def start(self):
        if self.vk_event.args is None:
            stream, _ = Service.objects.get_or_create(name="stream")
            stream_link = stream.value
            if len(stream_link) < 5:
                return "Стрим пока не идёт"
            else:
                return {'msg': stream_link, 'attachments': stream_link}
        else:
            self.check_sender(Role.MODERATOR)
            Service.objects.update_or_create(name="stream", defaults={'value': self.vk_event.args[0]})
            return "Ссылка изменена на " + self.vk_event.args[0]
