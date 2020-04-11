import requests


def get_detail_by_country(country_name, status='confirmed'):
    url = f"https://api.covid19api.com/dayone/country/{country_name}/status/{status}"
    response = requests.get(url).json()
    data = [x['Cases'] for x in response]
    date = [x['Date'] for x in response]
    return data, date


def get_by_country(country_name):
    def set_data(data):
        return f"Сегодня:\n" \
               f"Зараженные - {data['NewConfirmed']}, смерти - {data['NewDeaths']}, выздоровело - {data['NewRecovered']}\n" \
               f"Всего:\n" \
               f"Зараженные - {data['TotalConfirmed']}, смерти - {data['TotalDeaths']}, выздоровело - {data['TotalRecovered']}, болеют сейчас - {data['TotalConfirmed'] - data['TotalDeaths'] - data['TotalRecovered']}"

    url = f"https://api.covid19api.com/summary"
    response = requests.get(url).json()

    if country_name is None:
        return set_data(response["Global"])

    for country in response['Countries']:
        if country['Slug'].lower() == country_name.lower():
            return set_data(country)
    return None
