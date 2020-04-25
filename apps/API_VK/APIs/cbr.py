from xml.etree import ElementTree

import requests

URL = "https://www.cbr-xml-daily.ru/daily.xml"


def get_exchange_rates(_filters_list):
    response = requests.get(URL, stream=True)
    tree = ElementTree.fromstring(response.content)

    _filters = {x: 0 for x in _filters_list}
    for elem in tree:
        for _filter in _filters:
            if elem.find("CharCode").text == _filter:
                _filters[_filter] = float(elem.find("Value").text.replace(',', '.')) / float(
                    elem.find("Nominal").text.replace(',', '.'))
    return _filters
