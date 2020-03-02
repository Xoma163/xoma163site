from apps.API_VK.command.CommonCommand import CommonCommand
from apps.Statistics.models import Meme as MemeModel

IMAGE_EXTS = ['jpg', 'jpeg', 'png']


def check_name_exists(name):
    return MemeModel.objects.filter(name=name).exists()


class Meme(CommonCommand):
    def __init__(self):
        names = ["мем"]
        help_text = "Мем - присылает нужный мем"
        detail_help_text = "Мем (N) - присылает нужный мем. N = название мема.\n" \
                           "Добавление мема - /мем добавить ...(название) url\n" \
                           "Добавление мема - /мем добавить ...(название) (картинка)\n"
        super().__init__(names, help_text, detail_help_text, args=1)

    def send_1_meme(self, meme):
        if meme.link:
            if meme.link.find('vk.com') > 0 and meme.link.find('video'):
                att = meme.link[meme.link.find('video'):]
                return {'msg': '', 'attachments': [att]}
            return meme.link
        elif meme.image:
            photo = self.vk_bot.upload_photo(meme.image.path, False)
            return {'msg': '', 'attachments': [photo]}
        else:
            return "Какая-то хрень с мемом"

    def start(self):
        if self.vk_event.args[0] == 'добавить':
            self.check_args(2)

            if self.vk_event.attachments:
                new_meme = {'name': self.vk_event.original_args.split(' ', 1)[1], 'author': self.vk_event.sender}
                if check_name_exists(new_meme['name']):
                    return "Мем с таким названием уже есть"
                meme = MemeModel(**new_meme)
                meme.save()
                meme.save_remote_image(self.vk_event.attachments[0]['url'])
                return "Сохранил"
            elif len(self.vk_event.args) >= 3:
                new_meme = {'link': self.vk_event.args[-1], 'author': self.vk_event.sender}
                name = self.vk_event.original_args.split(' ', 1)[1]
                new_meme['name'] = name[:name.rfind(new_meme['link']) - 1]
                if check_name_exists(new_meme['name']):
                    return "Мем с таким названием уже есть"
                for meme_ext in IMAGE_EXTS:
                    # Если урл - картинка
                    if new_meme['link'].split('.')[-1].lower() == meme_ext:
                        link = new_meme.pop('link')
                        meme = MemeModel(**new_meme)
                        meme.save()
                        meme.save_remote_image(link)
                        return "Сохранил"

                MemeModel(**new_meme).save()
                return "Сохранил"
            else:
                return "Не передан url видео или не прикреплена картинка"
        else:
            # memes = MemeModel.objects.filter(name__icontains=self.vk_event.original_args)[:10]
            memes = MemeModel.objects.all()
            for arg in self.vk_event.args:
                memes = memes.filter(name__icontains=arg)
            if len(memes) == 0:
                # ToDo: Тонимото?
                return "Не нашёл :("
            elif len(memes) == 1:
                return self.send_1_meme(memes.first())
            else:
                for meme in memes:
                    if check_name_exists(meme.name):
                        return self.send_1_meme(meme)
                meme_names = [meme.name for meme in memes]
                meme_names_str = "\n".join(meme_names)
                return f"Нашёл сразу несколько, уточните:\n" \
                       f"{meme_names_str}"
