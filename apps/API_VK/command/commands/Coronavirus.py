from io import BytesIO
from threading import Lock

import matplotlib.pyplot as plt

from apps.API_VK.APIs.covid19api import get_by_country, get_detail_by_country
from apps.API_VK.APIs.yandex_translate import get_translate
from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import has_cyrillic

ALL_STATUSES = ['confirmed', 'recovered', 'deaths']
lock = Lock()


class Coronavirus(CommonCommand):

    def __init__(self):
        names = ["коронавирус", "корона", "вирус"]
        help_text = "Коронавирус - статистика по коронавирусу в разных странах"
        detail_help_text = "Коронавирус - статистика по коронавирусу в разных странах\n" \
                           "Коронавирус - статистика в мире\n" \
                           "Коронавирус ({название страны} [,график])- статистика в этой стране. С графиком или без\n"
        super().__init__(names, help_text, detail_help_text)

    def start(self):
        detail = False
        if self.vk_event.args:
            country = self.vk_event.args[0]
            if len(self.vk_event.args) >= 2:
                if self.vk_event.args[1].lower() == "график":
                    detail = 'Graphic'
                if self.vk_event.args[1].lower() in ["гист", "гистограмма", 'гиста', 'киста', 'глиста', 'коса',
                                                     'попса']:
                    detail = 'Gist'
        else:
            country = "Мир"

        if country != "Мир":
            if has_cyrillic(country):
                country_transliterate = get_translate('en', country).replace(' ', '-')
            else:
                country_transliterate = country
        else:
            country_transliterate = None

        if country.lower() in ["сша", "usa"]:
            country_transliterate = "united-states"

        result = get_by_country(country_transliterate)
        if result:
            msg = f"{country.capitalize()}\n\n{result}"
            if detail in ["Gist", "Graphic"]:
                attachments = []
                if detail == "Gist":
                    datas = [get_detail_by_country(country_transliterate, status) for status in ALL_STATUSES]

                    for i in range(len(datas[0][0])):
                        datas[0][0][i] -= datas[1][0][i] + datas[2][0][i]
                    fig, a = plt.subplots()
                    x = datas[0][1]
                    y1 = datas[0][0]
                    y2 = datas[2][0]
                    y2_bottom = y1
                    y3 = datas[1][0]
                    y3_bottom = [x + y for x, y in zip(datas[2][0], datas[0][0])]
                    a.bar(x, y1, label="Болеют", color="#46aada")
                    a.bar(x, y2, bottom=y2_bottom, label="Умершие", color="red")
                    a.bar(x, y3, bottom=y3_bottom, label="Выздоровевшие", color="green")
                    a.xaxis.set_visible(False)
                elif detail == "Graphic":
                    datas = [get_detail_by_country(country_transliterate, status)[0] for status in ALL_STATUSES]

                    max_len = max([len(x) for x in datas])
                    for i in range(len(datas)):
                        empty_list = [0] * (max_len - len(datas[i]))
                        datas[i] = empty_list + datas[i]

                    for i in range(len(datas[0])):
                        datas[0][i] -= datas[1][i] + datas[2][i]

                    plt.plot(datas[1], "bo-", label="Выздоровевшие", color="green")
                    plt.plot(datas[0], "bo-", label="Больные", color="#46aada")
                    plt.plot(datas[2], "bo-", label="Умершие", color="red")

                plt.title(country.capitalize())
                plt.xlabel('День')
                plt.ylabel('Количество людей')
                plt.legend()
                with lock:
                    graphic = BytesIO()
                    plt.savefig(graphic)
                    plt.cla()

                    attachment = self.vk_bot.upload_photo(graphic)
                    attachments.append(attachment)
                    return {'msg': msg, 'attachments': attachments}
            else:
                return msg
        else:
            return "Не нашёл такой страны"
