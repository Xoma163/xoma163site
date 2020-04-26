from django.core.paginator import Paginator

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.service.models import Meme as MemeModel


class Memes(CommonCommand):
    def __init__(self):
        names = ["мемы"]
        help_text = "Мемы - список мемов"
        detail_help_text = "Мемы [страница=1] - присылает список мемов на странице\n" \
                           "Мемы (поисковая фраза) - присылает список мемов, подходящих поисковому запросу"
        super().__init__(names, help_text, detail_help_text, api=False)

    def start(self):
        try:
            if self.vk_event.args:
                self.int_args = [0]
                self.parse_args('int')
                page = self.vk_event.args[0]
            else:
                page = 1

            memes = MemeModel.objects.all()
            p = Paginator(memes, 20)

            if page <= 0:
                page = 1
            if page > p.num_pages:
                page = p.num_pages

            msg_header = f"Страница {page}/{p.num_pages}"

            memes_on_page = p.page(page)
            meme_names = [meme.name for meme in memes_on_page]
            msg_body = ";\n".join(meme_names) + '.'

            if page != p.num_pages:
                on_last_page = p.per_page * page
            else:
                on_last_page = p.count
            msg_footer = f'----{p.per_page * (page - 1) + 1}/{on_last_page}----'
            msg = f"{msg_header}\n\n{msg_body}\n\n{msg_footer}"
            return msg
        except RuntimeError:
            memes = MemeModel.objects
            for arg in self.vk_event.args:
                memes = memes.filter(name__icontains=arg)
            memes_sliced = memes[:20]
            meme_names = [meme.name for meme in memes_sliced]
            meme_names_str = "\n".join(meme_names)
            if len(memes) > len(memes_sliced):
                meme_names_str += "\n..."
            return f"{meme_names_str}\n\nВсего - {len(memes)}"
