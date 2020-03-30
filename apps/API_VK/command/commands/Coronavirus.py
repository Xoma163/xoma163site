from threading import Lock

import matplotlib.pyplot as plt

from apps.API_VK.APIs.covid19api import get_by_country, get_detail_by_country
from apps.API_VK.APIs.yandex_translate import get_translate
from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import has_cyrillic
from xoma163site.settings import BASE_DIR

ALL_STATUSES = ['confirmed', 'recovered', 'deaths']
lock = Lock()


class Coronavirus(CommonCommand):

    def __init__(self):
        names = ["коронавирус", "корона", "вирус"]
        help_text = "Коронавирус - статистика по коронавирусу в разных странах"

        super().__init__(names, help_text)

    def start(self):
        detail = False
        if self.vk_event.args:
            country = self.vk_event.args[0]
            if len(self.vk_event.args) >= 2:
                if self.vk_event.args[1].lower() == "график":
                    detail = True
        else:
            country = "Россия"

        if has_cyrillic(country):
            country_transliterate = get_translate('en', country).replace(' ', '-')
        else:
            country_transliterate = country

        result = get_by_country(country_transliterate)
        if result:
            msg = f"{country.capitalize()}\n\n{result}"
            if detail:
                attachments = []
                datas = [get_detail_by_country(country_transliterate, status) for status in ALL_STATUSES]

                max_len = max([len(x) for x in datas])
                for i in range(len(datas)):
                    empty_list = [0] * (max_len - len(datas[i]))
                    datas[i] = empty_list + datas[i]

                plt.plot(datas[0], label="Больные")
                plt.plot(datas[1], label="Выздоровевшие")
                plt.plot(datas[2], label="Умершие")
                plt.xlabel('День')
                plt.ylabel('Количество людей')
                plt.legend()
                img_path = f"{BASE_DIR}/static/vkapi/coronavirus-{country_transliterate}.png"
                with lock:
                    plt.savefig(img_path)
                    plt.cla()

                    graphic = self.vk_bot.upload_photo(img_path)
                attachments.append(graphic)
                return {'msg': msg, 'attachments': attachments}
            else:
                return msg
        else:
            return "Не нашёл такой страны"
