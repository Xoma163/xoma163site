from itertools import groupby

import requests


def get_detail_by_country(country_name, status='confirmed'):
    url = f"https://api.covid19api.com/dayone/country/{country_name}/status/{status}"
    try:
        response = requests.get(url, timeout=10)
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
    data = [sum([y['Cases'] for y in x]) for x in groups]
    date = [x[0]['Date'] for x in groups]
    return data, date


def get_by_country(country_name):
    def set_data(data):
        return f"Сегодня:\n" \
               f"Заболело - {data['NewConfirmed']}\n" \
               f"Смертей - {data['NewDeaths']}\n" \
               f"Выздоровело - {data['NewRecovered']}\n\n" \
               f"На данный момент:\n" \
               f"Заболело - {data['TotalConfirmed']}\n" \
               f"Смертей- {data['TotalDeaths']}\n" \
               f"Выздоровело - {data['TotalRecovered']}\n" \
               f"Болеют сейчас - {data['TotalConfirmed'] - data['TotalDeaths'] - data['TotalRecovered']}\n"

    url = f"https://api.covid19api.com/summary"
    try:
        response = requests.get(url, timeout=5)
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
