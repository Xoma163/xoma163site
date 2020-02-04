from apps.API_VK.command.CommonCommand import CommonCommand
from apps.Statistics.models import Cat as CatModel
from xoma163site.settings import MAIN_SITE


class Cat(CommonCommand):
    def __init__(self):
        names = ["кот"]
        help_text = "Кот - добавить всратого кота в базу"
        detail_help_text = "Кот + вложение/пересылаемое сообщение с вложением - добавляет кота в БД"
        super().__init__(names, help_text, detail_help_text)

    def start(self):
        self.check_attachments()

        urls = []
        for attachment in self.vk_event.attachments:
            cat = CatModel()
            cat.get_remote_image(attachment['url'])
            cat.save()
            urls.append(MAIN_SITE + cat.image.url)
        return "\n".join(urls)
