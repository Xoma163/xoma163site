from itertools import groupby

import requests


def get_detail_by_country(country_name, status='confirmed'):
    url = f"https://api.covid19api.com/dayone/country/{country_name}/status/{status}"

    response = requests.get(url, timeout=5).json()
    groups = []
    for key, group in groupby(response, lambda x: x['Date']):
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
               f"Зараженные - {data['NewConfirmed']}, смерти - {data['NewDeaths']}, выздоровело - {data['NewRecovered']}\n" \
               f"Всего:\n" \
               f"Зараженные - {data['TotalConfirmed']}, смерти - {data['TotalDeaths']}, выздоровело - {data['TotalRecovered']}, болеют сейчас - {data['TotalConfirmed'] - data['TotalDeaths'] - data['TotalRecovered']}"

    url = f"https://api.covid19api.com/summary"
    response = requests.get(url, timeout=5).json()

    if country_name is None:
        return set_data(response["Global"])

    for country in response['Countries']:
        if country['Slug'].lower() == country_name.lower():
            return set_data(country)
    return None
