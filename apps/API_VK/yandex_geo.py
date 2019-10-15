import requests

from xoma163site.settings import BASE_DIR


def get_address(lat, lon):
    f = open(BASE_DIR + "/secrets/yandex_geo.txt")
    API_KEY = f.readline().strip()
    f.close()

    URL = "https://geocode-maps.yandex.ru/1.x/?apikey={}&geocode={},{}&format=json&sco=latlong&kind=house&results=1&lang=ru_RU".format(
        API_KEY, lat, lon)
    result = requests.get(URL).json()
    return \
    result['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData'][
        'text']
