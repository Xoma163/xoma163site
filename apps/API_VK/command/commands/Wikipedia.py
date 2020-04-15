import wikipedia

from apps.API_VK.command.CommonCommand import CommonCommand

wikipedia.set_lang("ru")


class Wikipedia(CommonCommand):
    def __init__(self):
        names = ["вики", "википедия"]
        help_text = "Вики - поиск информации в википедии"
        detail_help_text = "Вики ([{фраза}]) - поиск информации в википедии"
        super().__init__(names, help_text, detail_help_text, args=1)

    def start(self):
        try:
            page = wikipedia.page(self.vk_event.original_args)
            if page.summary != '':
                return page.summary
            else:
                return page.content
        except wikipedia.DisambiguationError as e:
            options = set(e.options)
            msg = "Нашел сразу несколько. Уточните\n"
            msg += "\n".join([x for x in options])
            return msg
        except wikipedia.PageError:
            msg = "Не нашёл такой страницы\n"
            search = wikipedia.search(self.vk_event.original_args)
            if len(search) == 0:
                msg += "Результат поиска ничего не дал"
            else:
                msg += "Я что-то нашёл, но так как такого кейса никогда не было, то я не знаю, что выводить, хд"
            return msg
