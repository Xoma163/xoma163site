from django.core.paginator import Paginator

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.service.models import Meme as MemeModel


class Memes(CommonCommand):
    def __init__(self):
        names = ["мемы"]
        help_text = "Мемы - список мемов"
        detail_help_text = "Мемы ([{фильтр}]) - присылает список мемов.\n" \
                           "Мемы ([{страница}]) - присылает список мемов на странице."
        super().__init__(names, help_text, detail_help_text, api=False, args=1)

    def start(self):
        try:
            self.int_args = [0]
            self.parse_args('int')

            page = self.vk_event.args[0]

            memes = MemeModel.objects.all()
            p = Paginator(memes, 20)

            if page <= 0:
                page = 1
            if page > p.num_pages:
                page = p.num_pages

            msg = f"Страница {page}/{p.num_pages}\n\n"
            memes_on_page = p.page(page)
            meme_names = [meme.name for meme in memes_on_page]
            meme_names_str = "\n".join(meme_names)
            return f"{msg}\n\n{meme_names_str}"
        except RuntimeError:
            memes = MemeModel.objects.all()
            for arg in self.vk_event.args:
                memes = memes.filter(name__icontains=arg)
