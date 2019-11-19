import requests


def get_joke(type=1):
    URL = "http://rzhunemogu.ru/RandJSON.aspx?CType={}".format(type)
    result = requests.get(URL)

    if result.status_code != 200:
        return "Чёто не работает. Пинайте этого лентяя"
    print(result.text)
    print(result.text.replace('{"content":"', '').replace('"}', ''))
    return result.text.replace('{"content":"', '').replace('"}', '')
