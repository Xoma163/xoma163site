from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.models import VkUser
from apps.service.models import City as CityModel


class City(CommonCommand):
    def __init__(self):
        names = ["город"]
        help_text = "Город - добавляет город в базу или устанавливает город пользователю"
        detail_help_text = "Город - устанавливает пользователю город, смотря его в профиле\n" \
                           "Город ({название}) - устанавливает пользователю город из аргумента\n" \
                           "Город добавить {название} {временная зона}(например Europe/Moscow, Europe/Samara) {широта} {долгота} \n" \
                           "Пример: /город добавить Самара Europe/Samara 53.212273 50.169435"
        super().__init__(names, help_text, detail_help_text)

    def start(self):

        if self.vk_event.args:
            if self.vk_event.args[0] == 'добавить':
                self.check_args(5)
                city_name = self.vk_event.args[1:len(self.vk_event.args) - 3]
                city_name = " ".join(city_name)
                city_timezone = self.vk_event.args[-3]
                self.float_args = [-2, -1]
                self.parse_args('float')
                city_lat = self.vk_event.args[-2]
                city_lon = self.vk_event.args[-1]

                city = CityModel.objects.filter(synonyms__icontains=city_name)
                if len(city) == 0:
                    city = CityModel(name=city_name, synonyms=city_name.lower(),
                                     timezone=city_timezone,
                                     lat=city_lat,
                                     lon=city_lon)
                    city.save()
                return "Добавил новый город"
            # Служебный метод для проставки всем юзерам города из профиля
            elif self.vk_event.args[0] == 'initial':
                self.check_sender('admin')
                users = VkUser.objects.all()
                for user in users:
                    vk_user = self.vk_bot.vk.users.get(user_id=user.user_id,
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
                    return "Не нашёл такого города. /город добавить {название} {часовой пояс} {длина} {широта}"
                else:
                    self.vk_event.sender.city = city
                    self.vk_event.sender.save()
                    return f"Изменил город на {city.name}"

        else:
            user = self.vk_bot.vk.users.get(user_id=self.vk_event.sender.user_id,
                                            lang='ru',
                                            fields='sex, bdate, city, screen_name')[0]
            if 'city' not in user:
                return "Город в профиле скрыт или не установлен. Пришлите название в аргументах"
            city = CityModel.objects.filter(synonyms__icontains=user['city']['title']).first()
            if not city:
                return "Не нашёл такого города. /город добавить {название} {часовой пояс} {длина} {широта}"
            else:
                self.vk_event.sender.city = city
                self.vk_event.sender.save()
                return f"Изменил город на {city.name}"
