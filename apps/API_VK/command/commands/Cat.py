from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import get_attachments_from_attachments_or_fwd, get_inline_keyboard
from apps.API_VK.command.Consts import Role
from apps.service.models import Cat as CatModel
from xoma163site.settings import MAIN_SITE


class Cat(CommonCommand):
    def __init__(self):
        names = ["кот"]
        help_text = "Кот - присылает рандомного всратого кота"
        detail_help_text = "Кот - присылает рандомного всратого кота\n\n" \
                           "Для доверенных:\n" \
                           "Кот (Изображения/Пересылаемое сообщение с изображениями) - добавляет кота в базу\n\n" \
                           "Для админа:\n" \
                           "Кот аватар - присылает нового кота для аватарки, которого ещё не было"
        super().__init__(names, help_text, detail_help_text)

    def add_cat(self, cat_image):
        cat = CatModel(author=self.vk_event.sender)
        cat.save_remote_image(cat_image['download_url'])
        cat.save()
        return MAIN_SITE + cat.image.url

    def start(self):
        if self.vk_event.args and self.vk_event.args[0].lower() in ['аватар']:
            self.check_sender(Role.ADMIN)
            cat = CatModel.objects.filter(to_send=True).order_by('?').first()
            cat.to_send = False
            cat.save()
            attachments = self.vk_bot.upload_photos(cat.image.path)
            return {'msg': "Держи нового кота на аватарку", 'attachments': attachments}

        images = get_attachments_from_attachments_or_fwd(self.vk_event, 'photo')

        if len(images) == 0:
            cat = CatModel.objects.filter().order_by('?').first()
            attachments = self.vk_bot.upload_photos(cat.image.path)

            return {
                'attachments': attachments,
                "keyboard": get_inline_keyboard(self.names[0])
            }
        else:
            self.check_sender(Role.TRUSTED)
            new_urls = []
            for image in images:
                new_url = self.add_cat(image)
                new_urls.append(new_url)
            return "\n".join(new_urls)
