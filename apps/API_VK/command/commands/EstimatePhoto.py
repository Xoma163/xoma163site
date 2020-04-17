from apps.API_VK.APIs.everypixel import get_image_quality
from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import get_att_from_attachments_or_fwd


class EstimatePhoto(CommonCommand):
    def __init__(self):
        names = ["оцени", "оценить"]
        help_text = "Оцени - оценить качество фотографии"
        detail_help_text = "Оцени (Пересылаемое сообщение) - оценивает качество изображения\n" \
                           "Оцени (Изображение) - оценивает качество изображения"
        super().__init__(names, help_text, detail_help_text, api=False)

    def start(self):
        image = get_att_from_attachments_or_fwd(self.vk_event, 'photo')

        if not image:
            return "Не нашёл картинки"

        return get_image_quality(image['url'])
