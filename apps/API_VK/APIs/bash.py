from bs4 import BeautifulSoup, NavigableString


def parse_bash(quotes_count):
    try:
        import requests
        from lxml import html
        r = requests.get('http://bash.im/random')
        bsop = BeautifulSoup(r.text, 'html.parser')
        html_quotes = bsop.find('section', {'class': 'quotes'}).find_all('div', {'class': 'quote__body'})[:quotes_count]
        bash_quotes = []

        for quote in html_quotes:
            text_quotes = []
            for content in quote.contents:
                if isinstance(content, NavigableString):
                    text_quotes.append(content.strip())
            bash_quotes.append("\n".join(text_quotes))
        return "\n——————————————————\n".join(bash_quotes)
    except Exception as e:
        print(e)
        return "Ошибка"
