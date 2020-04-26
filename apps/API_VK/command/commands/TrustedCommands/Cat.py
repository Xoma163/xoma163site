from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import get_attachments_from_attachments_or_fwd
from apps.service.models import Cat as CatModel
from xoma163site.settings import MAIN_SITE


class Cat(CommonCommand):
    def __init__(self):
        names = ["кот"]
        help_text = "Кот - добавить всратого кота в базу"
        detail_help_text = "Кот (Изображения/Пересылаемое сообщение с изображениями) - добавляет кота в БД"
        super().__init__(names, help_text, detail_help_text, access='trusted', api=False)

    def add_cat(self, cat_image):
        cat = CatModel(author=self.vk_event.sender)
        cat.save_remote_image(cat_image['download_url'])
        cat.save()
        return MAIN_SITE + cat.image.url

    def start(self):
        images = get_attachments_from_attachments_or_fwd(self.vk_event, 'photo')

        if len(images) == 0:
            return "Не нашёл картинок"
        new_urls = []
        for image in images:
            new_url = self.add_cat(image)
            new_urls.append(new_url)
        return "\n".join(new_urls)
