import requests


def get_detail_by_country(country_name, status='confirmed'):
    url = f"https://api.covid19api.com/dayone/country/{country_name}/status/{status}"
    response = requests.get(url).json()
    data = [x['Cases'] for x in response]
    return data


def get_by_country(country_name):
    url = f"https://api.covid19api.com/summary"
    response = requests.get(url).json()

    for country in response['Countries']:
        if country['Country'].lower() == country_name.lower():
            return f"Сегодня:\n" \
                   f"Зараженные - {country['NewConfirmed']}, смерти - {country['NewDeaths']}, выздоровело - {country['NewRecovered']}\n" \
                   f"Всего:\n" \
                   f"Зараженные - {country['TotalConfirmed']}, смерти - {country['TotalDeaths']}, выздоровело - {country['TotalRecovered']}"
    return None
