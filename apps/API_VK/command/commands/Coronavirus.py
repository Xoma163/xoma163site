from io import BytesIO
from threading import Lock

import matplotlib.pyplot as plt

from apps.API_VK.APIs.covid19api import get_by_country, get_detail_by_country
from apps.API_VK.APIs.yandex_translate import get_translate
from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import has_cyrillic

lock = Lock()


class Coronavirus(CommonCommand):
    def __init__(self):
        names = ["коронавирус", "корона", "вирус"]
        help_text = "Коронавирус - статистика по коронавирусу в разных странах"
        detail_help_text = "Коронавирус - статистика в мире\n" \
                           "Коронавирус [название страны [график/гистограмма]] - статистика в этой стране. С графиком " \
                           "или без\n"
        super().__init__(names, help_text, detail_help_text)

    def start(self):
        self.vk_bot.set_activity(self.vk_event.peer_id)

        detail = False
        if self.vk_event.args:
            country = self.vk_event.args[0]
            if len(self.vk_event.args) >= 2:
                if self.vk_event.args[1].lower() == "график":
                    detail = 'Graphic'
                _type = self.vk_event.args[1].lower()
                # ))
                if type in ["гист", "гистограмма"] or _type.endswith('ста') or _type.endswith('са'):
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
                self.api = False
                self.check_api()
                if detail == "Gist":
                    datas = get_detail_by_country(country_transliterate)
                    _, a = plt.subplots()
                    x = datas['Dates']
                    y1 = datas['Active']
                    y2 = datas['Deaths']
                    y3 = datas['Recovered']
                    y2_bottom = y1
                    y3_bottom = [x + y for x, y in zip(y1, y2)]
                    a.bar(x, y1, label="Болеют", color="#46aada", width=1)
                    a.bar(x, y2, bottom=y2_bottom, label="Умершие", color="red", width=1)
                    a.bar(x, y3, bottom=y3_bottom, label="Выздоровевшие", color="green", width=1)
                    a.xaxis.set_visible(False)
                elif detail == "Graphic":
                    datas = get_detail_by_country(country_transliterate)

                    # Возможно надо, яхз
                    # max_len = max([len(x) for x in datas])
                    # for i, _ in enumerate(datas):
                    #     empty_list = [0] * (max_len - len(datas[i]))
                    #     datas[i] = empty_list + datas[i]

                    plt.plot(datas['Recovered'], "bo-", label="Выздоровевшие", color="green")
                    plt.plot(datas['Active'], "bo-", label="Больные", color="#46aada")
                    plt.plot(datas['Deaths'], "bo-", label="Умершие", color="red")

                plt.title(country.capitalize())
                plt.xlabel('День')
                plt.ylabel('Количество людей')
                plt.legend()
                with lock:
                    graphic = BytesIO()
                    plt.savefig(graphic)
                    plt.cla()

                    attachments = self.vk_bot.upload_photos(graphic)
                    return {'msg': msg, 'attachments': attachments}
            else:
                return msg
        else:
            return "Не нашёл такой страны"
