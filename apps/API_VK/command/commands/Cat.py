from apps.API_VK.command.CommonCommand import CommonCommand
from apps.Statistics.models import Cat as CatModel
from xoma163site.settings import MAIN_SITE


def add_cat(cat_image):
    cat = CatModel()
    cat.get_remote_image(cat_image['url'])
    cat.author = cat_image['author']
    cat.save()
    return MAIN_SITE + cat.image.url


class Cat(CommonCommand):
    def __init__(self):
        names = ["кот"]
        help_text = "Кот - добавить всратого кота в базу"
        detail_help_text = "Кот + вложение/пересылаемое сообщение с вложением - добавляет кота в БД"
        super().__init__(names, help_text, detail_help_text, api=False)

    def start(self):
        from apps.API_VK.VkBotClass import parse_attachments

        if not (self.vk_event.attachments or self.vk_event.fwd):
            return "Пришлите фотографии или перешлите сообщения с фотографиями"

        cat_images = []
        if self.vk_event.attachments:
            for attachment in self.vk_event.attachments:
                cat_images.append({'url': attachment['url'], 'author': self.vk_event.sender})

        if self.vk_event.fwd:
            for msg in self.vk_event.fwd:
                attachments = parse_attachments(msg['attachments'])
                if attachments:
                    for attachment in attachments:
                        if msg['from_id'] > 0:
                            msg_user_id = int(msg['from_id'])
                            author = self.vk_bot.get_user_by_id(msg_user_id)
                        else:
                            author = None
                        cat_images.append({'url': attachment['url'], 'author': author})
        if len(cat_images) > 0:
            new_urls = []
            for cat_image in cat_images:
                new_url = add_cat(cat_image)
                new_urls.append(new_url)
            return "\n".join(new_urls)
        else:
            return "В пересланных сообщениях нет фотографий"
