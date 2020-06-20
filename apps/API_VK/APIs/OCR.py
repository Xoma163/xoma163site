import requests

from secrets.secrets import secrets


# https://ocr.space/OCRAPI
class OCRApi:
    def __init__(self):
        self.url = 'https://api.ocr.space/parse/image'
        self.api_key = secrets['ocr']['api_key']

    def recognize(self, image_url, lang):
        payload = {'url': image_url,
                   'apikey': self.api_key,
                   'language': lang,
                   }
        response = requests.post('https://api.ocr.space/parse/image',
                                 data=payload,
                                 ).json()
        if 'OCRExitCode' in response:
            if response['OCRExitCode'] == 99:
                raise RuntimeWarning("Неправильный язык")
        if 'ParsedResults' not in response:
            return "Ничего не распознал"
        text_list = [x['ParsedText'].strip() for x in response['ParsedResults']]
        texts = "\n".join(text_list)
        return texts
