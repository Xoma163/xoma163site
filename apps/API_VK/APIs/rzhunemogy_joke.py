import requests


def get_joke(_type=1):
    URL = f"http://rzhunemogu.ru/RandJSON.aspx"
    params = {
        'CType': _type
    }
    response = requests.get(URL, params, timeout=10)

    if response.status_code != 200:
        return "Чёто не работает. Пинайте этого лентяя"

    # Потому что от апи ответ гавённый и не jsonится
    return response.text.replace('{"content":"', '').replace('"}', '')
