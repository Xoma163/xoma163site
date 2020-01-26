from apps.API_VK.command.CommonCommand import CommonCommand


class ShortLinks(CommonCommand):
    def __init__(self):
        names = ["сс", "cc"]
        help_text = "̲С̲с N - сокращение ссылки N"
        super().__init__(names, help_text, need_args=True)

    def start(self):
        long_link = self.vk_event.args[0]
        short_link = self.vk_bot.get_short_link(long_link)
        if short_link:
            return short_link
        else:
            return "Пришлите ссылку"
