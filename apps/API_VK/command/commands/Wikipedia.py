import wikipedia

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import get_inline_keyboard

wikipedia.set_lang("ru")


class Wikipedia(CommonCommand):
    def __init__(self):
        names = ["вики", "википедия"]
        help_text = "Вики - поиск информации в википедии"
        detail_help_text = "Вики (фраза) - поиск информации в википедии"
        super().__init__(names, help_text, detail_help_text, args=1)

    def start(self):
        self.vk_bot.set_activity(self.vk_event.peer_id)

        is_random = False
        if self.vk_event.args[0].lower() in ["рандом", "р"]:
            is_random = True
            search_query = wikipedia.random()
        else:
            search_query = self.vk_event.original_args
        try:
            page = wikipedia.page(search_query)
            if page.summary != '':
                msg = f"{page.original_title}\n\n{page.summary}\n\nПодробнее: {page.url}"
            else:
                msg = f"{page.original_title}\n\n{page.content}\n\nПодробнее: {page.url}"
            if self.vk_event.from_api:
                return msg
            output = {'msg': msg, 'attachments': [page.url]}
            if page.images:
                output['attachments'] += self.vk_bot.upload_photos(page.images, 3)
            if is_random:
                output['keyboard'] = get_inline_keyboard(self.names[0], args={"random": "р"})
            return output
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
                msg += "Я нашел возможные варианты:\n"
                search = list(map(lambda x: f"- {x}", search))
                msg += "\n".join(search)
            return msg

# Если он серит в консоль, то
#  lib/wikipedia/wikipedia.py:389
#  lis = BeautifulSoup(html, 'html.parser').find_all('li')
