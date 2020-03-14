from apps.API_VK.command.CommonCommand import CommonCommand


class Bash(CommonCommand):
    def __init__(self):
        names = ["баш"]
        help_text = "Баш - рандомная цитата с баша"
        detail_help_text = "Баш [(N)] - рандомная цитата с баша. N - количество цитат. Максимум 25"
        super().__init__(names, help_text, detail_help_text, int_args=[0])

    def start(self):
        quotes_count = 5
        if self.vk_event.args:
            self.parse_int_args()
            quotes_count = self.vk_event.args[0]
            self.check_number_arg_range(quotes_count, 1, 25)
        return parse_bash(quotes_count)


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
