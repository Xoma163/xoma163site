import requests

from secrets.secrets import secrets

API_KEY = secrets['yandex']['geo']


def get_address(lat, lon):
    URL = f"https://geocode-maps.yandex.ru/1.x/?apikey={API_KEY}&geocode={lat},{lon}&format=json&sco=latlong&kind=house&results=1&lang=ru_RU"
    result = requests.get(URL).json()
    return \
        result['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty'][
            'GeocoderMetaData'][
            'text']
