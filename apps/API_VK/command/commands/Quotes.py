from django.core.paginator import Paginator

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.models import QuoteBook


def check_int_arg(arg):
    try:
        return int(arg), True
    except ValueError:
        return arg, False

class Quotes(CommonCommand):
    def __init__(self):
        names = ["цитаты"]
        help_text = "̲Ц̲и̲т̲а̲т̲ы [N[,M]]- просмотр сохранённых цитат. Возможные комбинации - N - номер страницы, N - фраза для поиска, N - фраза для поиска, M - номер страницы"
        super().__init__(names, help_text)

    def start(self):
        text_filter = None
        page = 1

        if self.vk_event.args is not None:
            if len(self.vk_event.args) >= 2:
                text_filter = " ".join(self.vk_event.args[:-1])

                page = self.vk_event.args[-1]
                page, result = check_int_arg(page)
                if not result:
                    page = 1
                self.check_int_arg_range(page, 0, float('inf'))

            elif len(self.vk_event.args) == 1:
                arg = self.vk_event.args[0]
                try:
                    arg = int(arg)
                    page = arg
                except ValueError:
                    text_filter = self.vk_event.args[0]

        if text_filter:
            objs = QuoteBook.objects.filter(text__icontains=text_filter)
        else:
            objs = QuoteBook.objects.all()

        objs = objs.filter(peer_id=self.vk_event.peer_id).order_by('-date')
        p = Paginator(objs, 5)

        if page > p.num_pages:
            page = p.num_pages

        objs_on_page = p.page(page)
        msg = "Страница {}/{}\n\n".format(page, p.num_pages)
        for i, obj_on_page in enumerate(objs_on_page):
            msg += "------------------------------{}------------------------------\n" \
                   "{}\n" \
                   "(c) {}\n".format(i + 1, obj_on_page.text, obj_on_page.date.strftime("%d.%m.%Y %H:%M:%S"))

        return msg
