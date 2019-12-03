import requests

from secrets.secrets import secrets


def get_address(lat, lon):
    API_KEY = secrets['yandex']['geo']


    URL = "https://geocode-maps.yandex.ru/1.x/?apikey={}&geocode={},{}&format=json&sco=latlong&kind=house&results=1&lang=ru_RU".format(
        API_KEY, lat, lon)
    result = requests.get(URL).json()
    return \
        result['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty'][
            'GeocoderMetaData'][
            'text']
