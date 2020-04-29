from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import get_inline_keyboard

MAX_QUOTES = 20


class Bash(CommonCommand):
    def __init__(self):
        names = ["баш"]
        help_text = "Баш - рандомная цитата с баша"
        detail_help_text = "Баш [количество=5] - рандомная цитата с баша. Максимум 25 цитат"
        super().__init__(names, help_text, detail_help_text, int_args=[0])

    def start(self):
        quotes_count = 5
        if self.vk_event.args:
            self.parse_int()
            quotes_count = self.vk_event.args[0]
            self.check_number_arg_range(quotes_count, 1, MAX_QUOTES)
        msg = parse_bash(quotes_count)
        if self.vk_event.from_api:
            return msg
        else:
            return {"msg": msg, "keyboard": get_inline_keyboard(self.names[0], args={"quotes_count": quotes_count})}


def parse_bash(quotes_count):
    try:
        import requests
        from lxml import html
        r = requests.get('http://bash.im/random')
        doc = html.document_fromstring(r.text)
        html_quotes = doc.xpath('//*[@class="quotes"]/article/div/div[@class="quote__body"]')
        bash_quotes = []
        for i in range(quotes_count):
            html_quote = "\n".join(html_quotes[i].xpath('text()'))
            bash_quotes.append(html_quote.strip('\n').strip(' ').strip('\n'))
        return "\n——————————————————\n".join(bash_quotes)
    except Exception as e:
        print(e)
        return "Ошибка"
