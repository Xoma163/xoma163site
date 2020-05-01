import requests


def get_joke(_type=1):
    URL = f"http://rzhunemogu.ru/RandJSON.aspx"
    params = {
        'CType': _type
    }
    try:
        response = requests.get(URL, params, timeout=10)
    except Exception as e:
        return f"Проблемы с апи. Подробности:\n{str(e)}"

    if response.status_code != 200:
        return "Чёто не работает. Пинайте этого лентяя"

    # Потому что от апи ответ гавённый и не jsonится
    return response.text.replace('{"content":"', '').replace('"}', '')
