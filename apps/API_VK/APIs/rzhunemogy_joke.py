import requests


def get_joke(type=1):
    URL = "http://rzhunemogu.ru/RandJSON.aspx?CType={}".format(type)
    try:
        result = requests.get(URL, timeout=10)
    except Exception as e:
        return "Проблемы с апи. Подробности:\n{}".format(str(e))

    if result.status_code != 200:
        return "Чёто не работает. Пинайте этого лентяя"

    return result.text.replace('{"content":"', '').replace('"}', '')
