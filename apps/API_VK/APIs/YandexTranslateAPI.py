import requests

from secrets.secrets import secrets


class YandexTranslateAPI:
    def __init__(self):
        self.url = "https://translate.yandex.net/api/v1.5/tr.json/translate"
        self.TOKEN = secrets['yandex']['translate']

    def get_translate(self, lang, text):
        params = {
            'lang': lang,
            'key': self.TOKEN,
            'text': text
        }
        response = requests.get(self.url, params).json()
        if response['code'] == 200:
            return response['text'][0]
        else:
            return f"Ошибка:\n{response}"
