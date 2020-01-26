from apps.API_VK.APIs.rebrandly import get_link
from apps.API_VK.command.CommonCommand import CommonCommand


class ShortLinks(CommonCommand):
    def __init__(self):
        names = ["сс", "cc"]
        help_text = "̲С̲с N - сокращение ссылки N"
        super().__init__(names, help_text, need_args=True)

    def start(self):
        #  ToDo: check on link

        long_link = self.vk_event.args[0]
        if 'http://' not in long_link or 'https//' not in long_link:
            long_link = f'http://{long_link}'
        short_link = get_link(long_link)
        if short_link:
            return short_link
        else:
            return "Пришлите ссылку"
