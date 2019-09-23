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

    import requests
    f = open(BASE_DIR + "/secrets/yandex.txt", "r")
    TOKEN = f.readline().strip()
    f.close()

    URL = "https://api.weather.yandex.ru/v1/informers?lat={}&lon={}&lang=ru_RU".format(lat, lon)
    HEADERS = {'X-Yandex-API-Key': TOKEN}
    result = requests.get(URL, headers=HEADERS).json()
    print(result)
    if 'status' in result:
        if result['status'] == 403:
            return "На сегодня я исчерпал все запросы к Yandex Weather :("
    WEATHER_TRANSLATE = {
        'clear': 'Ясно ☀',
        'partly-cloudy': 'Малооблачно ⛅',
        'cloudy': 'Облачно с прояснениями 🌥',
        'overcast': 'Пасмурно 🌧',
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

    WEATHER = {}
    WEATHER['now'] = {}
    WEATHER['now']['temp'] = result['fact']['temp']
    WEATHER['now']['temp_feels_like'] = result['fact']['feels_like']
    WEATHER['now']['condition'] = WEATHER_TRANSLATE[result['fact']['condition']]
    WEATHER['now']['wind_speed'] = result['fact']['wind_speed']
    WEATHER['now']['wind_gust'] = result['fact']['wind_gust']
    WEATHER['now']['pressure'] = result['fact']['pressure_mm']
    WEATHER['now']['humidity'] = result['fact']['humidity']

    WEATHER['forecast'] = {}
    WEATHER['forecast']['part_name'] = {}
    WEATHER['forecast']['temp_min'] = {}
    WEATHER['forecast']['temp_avg'] = {}
    WEATHER['forecast']['temp_max'] = {}
    WEATHER['forecast']['temp_feels_like'] = {}
    WEATHER['forecast']['condition'] = {}
    WEATHER['forecast']['wind_speed'] = {}
    WEATHER['forecast']['wind_gust'] = {}
    WEATHER['forecast']['pressure'] = {}
    WEATHER['forecast']['humidity'] = {}
    WEATHER['forecast']['prec_mm'] = {}
    WEATHER['forecast']['prec_period'] = {}
    WEATHER['forecast']['prec_prob'] = {}

    for i in range(len(result['forecast']['parts'])):
        WEATHER['forecast']['part_name'][i] = DAY_TRANSLATE[result['forecast']['parts'][i]['part_name']]
        WEATHER['forecast']['temp_min'][i] = result['forecast']['parts'][i]['temp_min']
        # WEATHER['forecast']['temp_avg'][i] = result['forecast']['parts'][i]['temp_avg']
        WEATHER['forecast']['temp_max'][i] = result['forecast']['parts'][i]['temp_max']
        WEATHER['forecast']['temp_feels_like'][i] = result['forecast']['parts'][i]['feels_like']
        WEATHER['forecast']['condition'][i] = WEATHER_TRANSLATE[result['forecast']['parts'][i]['condition']]
        WEATHER['forecast']['wind_speed'][i] = result['forecast']['parts'][i]['wind_speed']
        WEATHER['forecast']['wind_gust'][i] = result['forecast']['parts'][i]['wind_gust']
        WEATHER['forecast']['pressure'][i] = result['forecast']['parts'][i]['pressure_mm']
        WEATHER['forecast']['humidity'][i] = result['forecast']['parts'][i]['humidity']
        WEATHER['forecast']['prec_mm'][i] = result['forecast']['parts'][i]['prec_mm']
        WEATHER['forecast']['prec_period'][i] = int(result['forecast']['parts'][i]['prec_period']) / 60
        WEATHER['forecast']['prec_prob'][i] = result['forecast']['parts'][i]['prec_prob']

    now = 'Погода в {} сейчас:\n' \
          '{}\n' \
          'Температура {}°С(ощущается как {}°С)\n' \
          'Ветер {}м/c(порывы до {}м/c)\n' \
          'Давление {}мм.рт.ст., влажность - {}%'.format(
        city_name,
        WEATHER['now']['condition'], WEATHER['now']['temp'], WEATHER['now']['temp_feels_like'],
        WEATHER['now']['wind_speed'], WEATHER['now']['wind_gust'], WEATHER['now']['pressure'],
        WEATHER['now']['humidity'])

    forecast = ""
    for i in range(len(WEATHER['forecast']['prec_prob'])):
        forecast += '\n\n' \
                    'Прогноз на {}:\n' \
                    '{}\n' \
                    'Температура {}-{}°С(ощущается как {}°С)' \
                    '\nВетер {}м/c(порывы до {}м/c)\n' \
                    'Давление {} мм.рт.ст., влажность - {}%\n' \
                    'Осадки {}мм на протяжении {} часов с вероятностью {}%'.format(
            WEATHER['forecast']['part_name'][i],
            WEATHER['forecast']['condition'][i],
            WEATHER['forecast']['temp_min'][i], WEATHER['forecast']['temp_max'][i],
            WEATHER['forecast']['temp_feels_like'][i],
            WEATHER['forecast']['wind_speed'][i], WEATHER['forecast']['wind_gust'][i],
            WEATHER['forecast']['pressure'][i], WEATHER['forecast']['humidity'][i],
            WEATHER['forecast']['prec_mm'][i], WEATHER['forecast']['prec_period'][i],
            WEATHER['forecast']['prec_prob'][i]
        )
    return now + forecast
