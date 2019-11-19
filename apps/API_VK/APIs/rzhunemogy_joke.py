import json

import requests


def get_joke(type=1):
    URL = "http://rzhunemogu.ru/RandJSON.aspx?CType={}".format(type)
    result = requests.get(URL)

    if result.status_code != 200:
        return "Чёто не работает. Пинайте этого лентяя"

    result_text = result.text.replace('\r', '')
    result_json = json.loads(result_text, strict=False)
    return result_json['content']
