import requests
from bs4 import BeautifulSoup


class CBRAPI:
    def __init__(self, filters_list):
        self.filters = {x: {'name': None, 'value': 0} for x in filters_list}
        self.URL = "https://www.cbr-xml-daily.ru/daily.xml"

    def do(self):
        response = requests.get(self.URL, stream=True)
        elems = BeautifulSoup(response.content, 'xml').find('ValCurs').find_all("Valute")

        for elem in elems:
            for _filter in self.filters:
                if elem.find("CharCode").text == _filter:
                    self.filters[_filter]['name'] = elem.find('Name').text.lower()
                    self.filters[_filter]['value'] = float(elem.find("Value").text.replace(',', '.')) / float(
                        elem.find("Nominal").text.replace(',', '.'))

        return self.filters
