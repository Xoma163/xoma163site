import requests
from bs4 import BeautifulSoup

URL = "https://www.cbr-xml-daily.ru/daily.xml"


def get_exchange_rates(_filters_list):
    response = requests.get(URL, stream=True)
    elems = BeautifulSoup(response.content, 'xml').find('ValCurs').find_all("Valute")

    _filters = {x: {'name': None, 'value': 0} for x in _filters_list}
    for elem in elems:
        for _filter in _filters:
            if elem.find("CharCode").text == _filter:
                _filters[_filter]['name'] = elem.find('Name').text.lower()
                _filters[_filter]['value'] = float(elem.find("Value").text.replace(',', '.')) / float(
                    elem.find("Nominal").text.replace(',', '.'))

    return _filters
