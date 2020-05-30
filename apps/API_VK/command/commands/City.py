from apps.API_VK.APIs.TimezoneDBAPI import TimezoneDBAPI
from apps.API_VK.APIs.YandexGeoAPI import YandexGeoAPI
from apps.API_VK.command.CommonCommand import CommonCommand
from apps.service.models import City as CityModel, TimeZone


class City(CommonCommand):
    def __init__(self):
        names = ["город"]
        help_text = "Город - добавляет город в базу или устанавливает город пользователю"
        detail_help_text = "Город - устанавливает пользователю город, смотря его в профиле\n" \
                           "Город [название] - устанавливает пользователю город из аргумента\n" \
                           "Город добавить (название города)\n"
        super().__init__(names, help_text, detail_help_text)

    def start(self):

        if self.vk_event.args:
            if self.vk_event.args[0] == 'добавить':
                self.check_args(2)
                city_name = self.vk_event.args[1:len(self.vk_event.args)]
                city_name = " ".join(city_name)
                city = add_city_to_db(city_name)
                return f"Добавил новый город - {city.name}"
            else:
                city_name = self.vk_event.args[0]
                city = CityModel.objects.filter(synonyms__icontains=city_name).first()
                if not city:
                    return "Не нашёл такого города. /город добавить (название города)"
                else:
                    self.vk_event.sender.city = city
                    self.vk_event.sender.save()
                    return f"Изменил город на {city.name}"
        else:
            if self.vk_event.sender.city is not None:
                return f"Ваш город - {self.vk_event.sender.city}"
            user = self.vk_bot.vk.users.get(user_id=self.vk_event.sender.user_id,
                                            lang='ru',
                                            fields='city')[0]
            if 'city' not in user:
                return "Город в профиле скрыт или не установлен. Пришлите название в аргументах - /город (название " \
                       "города)"

            city = CityModel.objects.filter(synonyms__icontains=user['city']['title']).first()
            if not city:
                city = add_city_to_db(user['city']['title'])
            self.vk_event.sender.city = city
            self.vk_event.sender.save()
            return f"Изменил город на {city.name}"


def add_city_to_db(city_name):
    yandexgeo_api = YandexGeoAPI()
    city_info = yandexgeo_api.get_city_info_by_name(city_name)
    if not city_info:
        raise RuntimeError("Не смог найти координаты для города")
    city = CityModel.objects.filter(name=city_info['name'])
    if len(city) != 0:
        raise RuntimeError("Такой город уже есть")
    city_info['synonyms'] = city_info['name'].lower()
    timezonedb_api = TimezoneDBAPI()
    timezone_name = timezonedb_api.get_timezone_by_coordinates(city_info['lat'], city_info['lon'])
    if not timezone_name:
        raise RuntimeError("Не смог найти таймзону для города")
    timezone_obj, _ = TimeZone.objects.get_or_create(name=timezone_name)

    city_info['timezone'] = timezone_obj
    city = CityModel(**city_info)
    city.save()
    return city
