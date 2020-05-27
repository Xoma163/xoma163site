import time
from itertools import groupby

import requests

TRIES = 10


def do_the_request(url, **kwargs):
    tries = TRIES
    status_code = None
    response = None
    while tries > 0 and status_code != 200:
        response = requests.get(url, **kwargs)
        tries -= 1
        status_code = response.status_code
        time.sleep(1)
    return response


def get_detail_by_country(country_name):
    url = f"https://api.covid19api.com/dayone/country/{country_name}"
    try:
        response = do_the_request(url, timeout=20)
        time.sleep(1)
    except requests.exceptions.ReadTimeout:
        raise RuntimeError("Проблемы с API. Слишком долго ждал")
    if not response:
        raise RuntimeError(f"Проблемы с API. {response.status_code}")
    response = response.json()
    groups = []
    for _, group in groupby(response, lambda x: x['Date']):
        list_group = list(group)
        if len(list_group) > 0:
            groups.append(list_group)

    # Суммирование сгрупированных данных
    data = {'Confirmed': [], 'Deaths': [], "Recovered": [], "Dates": []}
    for group in groups:
        confirmed = sum([x['Confirmed'] for x in group])
        deaths = sum([x['Deaths'] for x in group])
        recovered = sum([x['Recovered'] for x in group])
        data['Confirmed'].append(confirmed - deaths - recovered)
        data['Deaths'].append(deaths)
        data['Recovered'].append(recovered)
        data['Dates'].append(group[0]['Date'])
    return data


def get_by_country(country_name):
    def set_data(data):
        return f"Сегодня:\n" \
               f"Заболело - {data['NewConfirmed']}\n" \
               f"Смертей - {data['NewDeaths']}\n" \
               f"Выздоровело - {data['NewRecovered']}\n\n" \
               f"На данный момент:\n" \
               f"Заболело - {data['TotalConfirmed']}\n" \
               f"Смертей - {data['TotalDeaths']}\n" \
               f"Выздоровело - {data['TotalRecovered']}\n" \
               f"Болеют сейчас - {data['TotalConfirmed'] - data['TotalDeaths'] - data['TotalRecovered']}\n"

    url = f"https://api.covid19api.com/summary"
    try:
        response = do_the_request(url, timeout=10)
    except requests.exceptions.ReadTimeout:
        raise RuntimeError("Проблемы с API. Слишком долго ждал")
    if not response:
        raise RuntimeError(f"Проблемы с API. {response.status_code}")
    response = response.json()

    if country_name is None:
        return set_data(response["Global"])

    for country in response['Countries']:
        if country['Slug'].lower() == country_name.lower():
            return set_data(country)
    return None
