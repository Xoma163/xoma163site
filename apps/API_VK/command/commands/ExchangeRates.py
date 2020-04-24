from xml.etree import ElementTree

import requests

from apps.API_VK.command.CommonCommand import CommonCommand


class ExchangeRates(CommonCommand):
    def __init__(self):
        names = ["курс"]
        help_text = "Курс - курс валют"
        super().__init__(names, help_text)

    def start(self):
        response = requests.get("https://www.cbr-xml-daily.ru/daily.xml")
        tree = ElementTree.fromstring(response.content)

        _filters = {"USD": 0, "EUR": 0}
        for elem in tree:
            for _filter in _filters:
                if elem.find("CharCode").text == _filter:
                    _filters[_filter] = elem.find("Value").text

        msg = "Курс валют:\n"
        for _filter in _filters:
            _filters[_filter] = round(float(_filters[_filter].replace(',', '.')), 2)
            msg += f"{_filter} - {_filters[_filter]} руб.\n"
        return msg
