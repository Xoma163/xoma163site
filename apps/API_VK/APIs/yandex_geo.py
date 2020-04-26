import requests

from secrets.secrets import secrets

API_KEY = secrets['yandex']['geo']


def get_address(lat, lon):
    URL = f"https://geocode-maps.yandex.ru/1.x/"
    params = {
        'apikey': API_KEY,
        'geocode': f"{lat, lon}",
        'format': 'json',
        'result': '1',
        'lang': 'ru_RU'
    }
    result = requests.get(URL, params).json()
    return result['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty'][
        'GeocoderMetaData']['text']


def get_city_info_by_name(city_name):
    URL = f"https://geocode-maps.yandex.ru/1.x/"
    params = {
        'apikey': API_KEY,
        'geocode': city_name,
        'format': 'json',
        'result': '1',
        'lang': 'ru_RU'
    }
    result = requests.get(URL, params).json()
    result2 = result['response']['GeoObjectCollection']['featureMember']
    if len(result2) == 0:
        return None
    city_data = result2[0]['GeoObject']
    lon, lat = city_data['Point']['pos'].split(' ', 2)
    city_name = city_data['name']
    city_info = {
        'lat': lat,
        'lon': lon,
        'name': city_name
    }
    return city_info
