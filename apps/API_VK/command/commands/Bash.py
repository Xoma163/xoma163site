from apps.API_VK.APIs.BashAPI import BashAPI
from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import get_inline_keyboard

MAX_QUOTES = 20


class Bash(CommonCommand):
    def __init__(self):
        names = ["баш"]
        help_text = "Баш - рандомная цитата с баша"
        detail_help_text = "Баш [количество=5] - рандомная цитата с баша. Максимум 20 цитат"
        super().__init__(names, help_text, detail_help_text, int_args=[0])

    def start(self):
        quotes_count = 5
        if self.vk_event.args:
            self.parse_int()
            quotes_count = self.vk_event.args[0]
            self.check_number_arg_range(quotes_count, 1, MAX_QUOTES)
        bash_api = BashAPI(quotes_count)
        msg = bash_api.parse()
        if self.vk_event.from_api:
            return msg
        else:
            return {"msg": msg, "keyboard": get_inline_keyboard(self.names[0], args={"quotes_count": quotes_count})}
