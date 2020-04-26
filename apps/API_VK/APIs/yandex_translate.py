import requests

from secrets.secrets import secrets

TOKEN = secrets['yandex']['translate']


def get_translate(lang, text):
    URL = f"https://translate.yandex.net/api/v1.5/tr.json/translate"
    params = {
        'lang': lang,
        'key': TOKEN,
        'text': text
    }
    response = requests.get(URL, params).json()
    if response['code'] == 200:
        return response['text'][0]
    else:
        return f"Ошибка:\n{response}"
