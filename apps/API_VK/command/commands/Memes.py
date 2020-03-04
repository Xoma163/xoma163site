from apps.API_VK.command.CommonCommand import CommonCommand
from apps.service.models import Meme as MemeModel


class Memes(CommonCommand):
    def __init__(self):
        names = ["мемы"]
        help_text = "Мемы - список мемов"
        detail_help_text = "Мемы ([N]) - присылает список мемов. N = фильтр для поиска"
        super().__init__(names, help_text, detail_help_text)

    def start(self):
        if self.vk_event.args:
            memes = MemeModel.objects.all()
            for arg in self.vk_event.args:
                memes = memes.filter(name__icontains=arg)
            # memes = MemeModel.objects.filter(name__icontains=self.vk_event.original_args)
        else:
            memes = MemeModel.objects.all()
        meme_names = [meme.name for meme in memes]
        if len(meme_names) > 20:
            meme_names = meme_names[:20]
            meme_names.append('...')
        meme_names_str = "\n".join(meme_names)
        return f"{meme_names_str}\n\nВсего - {len(memes)}"
