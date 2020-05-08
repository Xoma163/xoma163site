import vk_api

from apps.API_VK.command.CommonCommand import CommonCommand


class ShortLinks(CommonCommand):
    def __init__(self):
        names = ["сс", "cc"]
        help_text = "Сс - сокращение ссылки"
        detail_help_text = "Сс (ссылка) - сокращение ссылки\n" \
                           "Сс (Пересылаемое сообщение) - сокращение ссылки"
        super().__init__(names, help_text, detail_help_text, args=1)

    def start(self):
        msgs = self.vk_event.fwd
        if msgs:
            long_link = self.vk_event.fwd[0]['text']
        else:
            long_link = self.vk_event.args[0]
        try:
            short_link = self.vk_bot.get_short_link(long_link)
        except vk_api.ApiError:
            return "Неверный формат ссылки"
        return short_link
