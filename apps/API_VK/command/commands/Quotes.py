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
        help_text = "Цитаты - просмотр сохранённых цитат"
        detail_help_text = "Цитаты [N[,M]] - просмотр сохранённых цитат. Возможные комбинации: \n" \
                           "1) N - номер страницы;\n" \
                           "2) N - фраза для поиска;\n" \
                           "3) N - фраза для поиска M - номер страницы"
        super().__init__(names, help_text, detail_help_text)

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
                self.check_number_arg_range(page, 0, float('inf'))

            elif len(self.vk_event.args) == 1:
                arg = self.vk_event.args[0]
                try:
                    arg = int(arg)
                    page = arg
                except ValueError:
                    text_filter = self.vk_event.args[0]

        if self.vk_event.chat:
            objs = QuoteBook.objects.filter(vk_chat=self.vk_event.chat)
        else:
            objs = QuoteBook.objects.filter(vk_user=self.vk_event.sender)

        if text_filter:
            objs = objs.filter(text__icontains=text_filter)
        objs = objs.order_by('-date')
        p = Paginator(objs, 5)

        if page <= 0:
            page = 1
        if page > p.num_pages:
            page = p.num_pages

        objs_on_page = p.page(page)
        msg = f"Страница {page}/{p.num_pages}\n\n"
        for i, obj_on_page in enumerate(objs_on_page):
            if not self.vk_event.from_api:
                msg += f"------------------------------{i + 1}------------------------------\n" \
                       f"{obj_on_page.text}\n" \
                       f"(c) {obj_on_page.date.strftime('%d.%m.%Y %H:%M:%S')}\n"
            else:
                msg += f"Цитата #{i + 1}\n" \
                       f"{obj_on_page.text}\n" \
                       f"(c) {obj_on_page.date.strftime('%d.%m.%Y %H:%M:%S')}\n"

        return msg
