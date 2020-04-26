import requests

from secrets.secrets import secrets

API_KEY = secrets['timezonedb']['api_key']


def get_timezone_by_coordinates(lat, lon):
    URL = "http://api.timezonedb.com/v2.1/get-time-zone"
    params = {
        'key': API_KEY,
        'format': 'json',
        'by': 'position',
        'lat': lat,
        'lng': lon
    }
    result = requests.get(URL, params=params).json()
    return result['zoneName']
