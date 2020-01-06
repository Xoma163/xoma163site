import requests

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import has_cyrillic
from secrets.secrets import secrets


class Translate(CommonCommand):
    def __init__(self):
        names = ["перевод"]
        help_text = "̲П̲е̲р̲е̲в̲о̲д [N] (N - фраза) - англо-русский переводчик"
        super().__init__(names, help_text)

    def start(self):
        fwd = self.vk_event.fwd
        if not fwd:
            if not self.vk_event.original_args:
                return "Требуется аргументы или пересылаемые сообщения"

            text = self.vk_event.original_args
        else:
            text = ""
            for msg in fwd:
                text += "{}\n".format(msg['text'])

        if has_cyrillic(text):
            lang = 'ru-en'
        else:
            lang = 'en-ru'
        TOKEN = secrets['yandex']['translate']

        URL = "https://translate.yandex.net/api/v1.5/tr.json/translate?lang={} &key={}&text={}".format(lang, TOKEN,
                                                                                                       text)
        response = requests.get(URL).json()
        if response['code'] == 200:
            return response['text'][0]
        else:
            return "Ошибка:\n{}".format(response)
