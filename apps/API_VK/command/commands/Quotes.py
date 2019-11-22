from django.core.paginator import Paginator

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.models import QuoteBook


class Quotes(CommonCommand):
    def __init__(self):
        names = ["цитаты"]
        help_text = "̲Ц̲и̲т̲а̲т̲ы [N[,M]]- просмотр сохранённых цитат. Возможные комбинации - N - номер страницы, N - фраза для поиска, N - фраза для поиска, M - номер страницы"
        super().__init__(names, help_text)

    def start(self):
        text_filter = None

        if self.vk_event.args is not None:
            if len(self.vk_event.args) == 2:
                try:
                    page = int(self.vk_event.args[1])
                except:
                    self.vk_bot.send_message(self.vk_event.chat_id, "Номер страницы должен быть целочисленным")
                    return
                if page <= 0:
                    self.vk_bot.send_message(self.vk_event.chat_id, "Номер страницы должен быть положительным")
                    return
                text_filter = self.vk_event.args[0]
            elif len(self.vk_event.args) == 1:
                try:
                    page = int(self.vk_event.args[0])
                    if page <= 0:
                        self.vk_bot.send_message(self.vk_event.chat_id, "Номер страницы должен быть положительным")
                        return
                except:
                    page = 1
                    text_filter = self.vk_event.args[0]
            else:
                self.vk_bot.send_message(self.vk_event.chat_id, "Неверное количество аргументов")
                return

            if text_filter is not None:
                objs = QuoteBook.objects.filter(text__icontains=text_filter)
            else:
                objs = QuoteBook.objects.all()
        else:
            objs = QuoteBook.objects.all()
            page = 1
        objs = objs.filter(peer_id=self.vk_event.peer_id).order_by('-date')
        p = Paginator(objs, 5)

        if page > p.num_pages:
            self.vk_bot.send_message(self.vk_event.chat_id,
                                     "Такой страницы нет. Последняя страница - {}".format(p.num_pages))
            return

        objs_on_page = p.page(page)
        msg = "Страница {}/{}\n\n".format(page, p.num_pages)
        for i, obj_on_page in enumerate(objs_on_page):
            msg += "------------------------------{}------------------------------\n" \
                   "{}\n" \
                   "(c) {}\n".format(i + 1, obj_on_page.text, obj_on_page.date.strftime("%d.%m.%Y %H:%M:%S"))

        self.vk_bot.send_message(self.vk_event.chat_id, msg)
