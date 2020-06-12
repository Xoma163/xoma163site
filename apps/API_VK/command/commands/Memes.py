from django.core.paginator import Paginator

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import check_user_group
from apps.API_VK.command.Consts import Role
from apps.API_VK.command.commands.Meme import get_tanimoto_memes
from apps.service.models import Meme as MemeModel


def get_memes_names(memes, sender):
    if check_user_group(sender, Role.MODERATOR):
        meme_names = [f"{meme.name} (id - {meme.id})" for meme in memes]
    else:
        meme_names = [meme.name for meme in memes]
    return meme_names


class Memes(CommonCommand):
    def __init__(self):
        names = ["мемы"]
        help_text = "Мемы - список мемов"
        detail_help_text = "Мемы [страница=1] - присылает список мемов на странице\n" \
                           "Мемы (поисковая фраза) - присылает список мемов, подходящих поисковому запросу\n\n"

        super().__init__(names, help_text, detail_help_text)

    def start(self):
        try:
            if self.vk_event.args:
                self.int_args = [0]
                self.parse_int()
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
            meme_names = get_memes_names(memes_on_page, self.vk_event.sender)
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
            if len(memes) == 0:
                return "Не нашёл мемов по заданному запросу"
            memes = get_tanimoto_memes(memes, self.vk_event.original_args)
            memes_sliced = memes[:20]
            meme_names = get_memes_names(memes_sliced, self.vk_event.sender)
            meme_names_str = ";\n".join(meme_names)
            if len(memes) > len(memes_sliced):
                meme_names_str += "\n..."
            else:
                meme_names_str += '.'
            return f"{meme_names_str}\n\nВсего - {len(memes)}"
