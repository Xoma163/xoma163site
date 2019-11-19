import requests

from xoma163site.settings import BASE_DIR


def get_weather(city="самара"):
    if city == "самара":
        city_name = "Самаре"
        lat = 53.212273
        lon = 50.169435
    elif city in ['питер', 'санкт-петербург', 'питере', 'санкт-петербурге', 'спб']:
        city_name = "Питере"
        lat = 59.939095
        lon = 30.315868
    elif city in ['сызрань', 'сызрани']:
        city_name = "Сызрани"
        lat = 53.155782
        lon = 48.474485
    elif city in ['прибой', 'прибое']:
        city_name = "Прибое"
        lat = 52.8689435
        lon = 49.6516931
    elif city in ['купчино']:
        city_name = "Купчино"
        lat = 59.872380
        lon = 30.370291
    else:
        return 'Я не знаю координат города {}. Сообщите их разработчику'.format(city)

    f = open(BASE_DIR + "/secrets/yandex_weather.txt")
    TOKEN = f.readline().strip()
    f.close()

    URL = "https://api.weather.yandex.ru/v1/informers?lat={}&lon={}&lang=ru_RU".format(lat, lon)
    HEADERS = {'X-Yandex-API-Key': TOKEN}
    result = requests.get(URL, headers=HEADERS).json()
    if 'status' in result:
        if result['status'] == 403:
            return "На сегодня я исчерпал все запросы к Yandex Weather :("
    WEATHER_TRANSLATE = {
        'clear': 'Ясно ☀',
        'partly-cloudy': 'Малооблачно ⛅',
        'cloudy': 'Облачно с прояснениями 🌥',
        'overcast': 'Пасмурно ☁',
        'partly-cloudy-and-light-rain': 'Небольшой дождь 🌧',
        'partly-cloudy-and-rain': 'Дождь 🌧',
        'overcast-and-rain': 'Сильный дождь 🌧🌧',
        'overcast-thunderstorms-with-rain': 'Сильный дождь, гроза 🌩',
        'cloudy-and-light-rain': 'Небольшой дождь 🌧',
        'overcast-and-light-rain': 'Небольшой дождь 🌧',
        'cloudy-and-rain': 'Дождь 🌧',
        'overcast-and-wet-snow': 'Дождь со снегом 🌨',
        'partly-cloudy-and-light-snow': 'Небольшой снег 🌨',
        'partly-cloudy-and-snow': 'Снег 🌨',
        'overcast-and-snow': 'Снегопад 🌨',
        'cloudy-and-light-snow': 'Небольшой снег 🌨',
        'overcast-and-light-snow': 'Небольшой снег 🌨',
        'cloudy-and-snow': 'Снег 🌨'}
    DAY_TRANSLATE = {
        'night': 'ночь',
        'morning': 'утро',
        'day': 'день',
        'evening': 'вечер',
    }

    weather = {
        'now': {
            'temp': result['fact']['temp'],
            'temp_feels_like': result['fact']['feels_like'],
            'condition': WEATHER_TRANSLATE[result['fact']['condition']],
            'wind_speed': result['fact']['wind_speed'],
            'wind_gust': result['fact']['wind_gust'],
            'pressure': result['fact']['pressure_mm'],
            'humidity': result['fact']['humidity'],
        },
        'forecast': {}}

    for i in range(len(result['forecast']['parts'])):
        weather['forecast'][i] = {
            'part_name': DAY_TRANSLATE[result['forecast']['parts'][i]['part_name']],
            'temp_min': result['forecast']['parts'][i]['temp_min'],
            'temp_max': result['forecast']['parts'][i]['temp_max'],
            'temp_feels_like': result['forecast']['parts'][i]['feels_like'],
            'condition': WEATHER_TRANSLATE[result['forecast']['parts'][i]['condition']],
            'wind_speed': result['forecast']['parts'][i]['wind_speed'],
            'wind_gust': result['forecast']['parts'][i]['wind_gust'],
            'pressure': result['forecast']['parts'][i]['pressure_mm'],
            'humidity': result['forecast']['parts'][i]['humidity'],
            'prec_mm': result['forecast']['parts'][i]['prec_mm'],
            'prec_period': int(int(result['forecast']['parts'][i]['prec_period']) / 60),
            'prec_prob': result['forecast']['parts'][i]['prec_prob'],
        }

    now = 'Погода в {} сейчас:\n' \
          '{}\n' \
          'Температура {}°С(ощущается как {}°С)\n' \
          'Ветер {}м/c(порывы до {}м/c)\n' \
          'Давление  {}мм.рт.ст., влажность {}%'.format(city_name,
                                                        weather['now']['condition'], weather['now']['temp'],
                                                        weather['now']['temp_feels_like'],
                                                        weather['now']['wind_speed'], weather['now']['wind_gust'],
                                                        weather['now']['pressure'],
                                                        weather['now']['humidity'])

    forecast = ""
    for i in range(len(weather['forecast'])):
        forecast += '\n\n' \
                    'Прогноз на {}:\n' \
                    '{}\n'.format(
            weather['forecast'][i]['part_name'],
            weather['forecast'][i]['condition'])

        if weather['forecast'][i]['temp_min'] != weather['forecast'][i]['temp_max']:
            forecast += 'Температура от {} до {}°С'.format(weather['forecast'][i]['temp_min'],
                                                           weather['forecast'][i]['temp_max'])
        else:
            forecast += 'Температура {}°С'.format(weather['forecast'][i]['temp_max'])

        forecast += '(ощущается как {}°С)\n' \
                    'Ветер {}м/c(порывы до {}м/c)\n' \
                    'Давление {} мм.рт.ст., влажность {}%\n'.format(weather['forecast'][i]['temp_feels_like'],
                                                                    weather['forecast'][i]['wind_speed'],
                                                                    weather['forecast'][i]['wind_gust'],
                                                                    weather['forecast'][i]['pressure'],
                                                                    weather['forecast'][i]['humidity']
                                                                    )
        if weather['forecast'][i]['prec_mm'] != 0:
            forecast += 'Осадки {}мм на протяжении {} часов с вероятностью {}%'.format(
                weather['forecast'][i]['prec_mm'],
                weather['forecast'][i]['prec_period'],
                weather['forecast'][i]['prec_prob'])
        else:
            forecast += "Без осадков"
    return now + forecast
