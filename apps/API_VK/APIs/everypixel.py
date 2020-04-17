import requests

from secrets.secrets import secrets

CLIENT_ID = secrets['everypixel']['client_id']
CLIENT_SECRET = secrets['everypixel']['client_secret']


def get_image_quality(image_url):
    params = {'url': image_url}
    response = requests.get('https://api.everypixel.com/v1/quality_ugc',
                            params=params,
                            auth=(CLIENT_ID, CLIENT_SECRET)).json()

    if response['status'] == 'error':
        print(response)
        return "Ошибка"
    elif response['status'] == 'ok':
        return f"{round(response['quality']['score'] * 100, 2)}%"
    else:
        return "Wtf"


def get_faces_on_photo(image_url):
    params = {'url': image_url}
    response = requests.get('https://api.everypixel.com/v1/faces',
                            params=params,
                            auth=(CLIENT_ID, CLIENT_SECRET)).json()
    return response
