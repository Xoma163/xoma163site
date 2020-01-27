from vk_api import ApiError

from apps.API_VK.command.CommonCommand import CommonCommand


class ShortLinks(CommonCommand):
    def __init__(self):
        names = ["сс", "cc"]
        help_text = "̲С̲с N - сокращение ссылки N"
        super().__init__(names, help_text)

    def start(self):
        msgs = self.vk_event.fwd
        if msgs:
            long_link = self.vk_event.fwd[0]['text']
        else:
            long_link = self.vk_event.args[0]
        try:
            short_link = self.vk_bot.get_short_link(long_link)
        except ApiError:
            return "Неверный формат ссылки"
        return short_link
