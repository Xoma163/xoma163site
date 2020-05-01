from apps.API_VK.APIs.timezonedb import get_timezone_by_coordinates
from apps.API_VK.APIs.yandex_geo import get_city_info_by_name
from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.models import VkUser
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
            elif self.vk_event.args[0] == 'initial':
                self.check_sender('admin')
                users = VkUser.objects.all().exclude(user_id='ANONYMOUS')
                for user in users:
                    vk_user = self.vk_bot.vk.users.get(user_id=int(user.user_id),
                                                       lang='ru',
                                                       fields='sex, bdate, city, screen_name')[0]
                    if 'city' in vk_user:
                        city = CityModel.objects.filter(synonyms__icontains=vk_user['city']['title'])
                        if len(city) > 0:
                            user.city = city.first()
                            user.save()
                return 'done'
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
            user = self.vk_bot.vk.users.get(user_id=self.vk_event.sender.user_id,
                                            lang='ru',
                                            fields='sex, bdate, city, screen_name')[0]
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
    city_info = get_city_info_by_name(city_name)
    if not city_info:
        raise RuntimeError("Не смог найти координаты для города")
    city = CityModel.objects.filter(name=city_info['name'])
    if len(city) != 0:
        raise RuntimeError("Такой город уже есть")
    city_info['synonyms'] = city_info['name'].lower()
    timezone_name = get_timezone_by_coordinates(city_info['lat'], city_info['lon'])
    if not timezone_name:
        raise RuntimeError("Не смог найти таймзону для города")
    timezone_obj, _ = TimeZone.objects.get_or_create(name=timezone_name)

    city_info['timezone'] = timezone_obj
    city = CityModel(**city_info)
    city.save()
    return city
