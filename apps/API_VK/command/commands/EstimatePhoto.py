from apps.API_VK.APIs.EveryPixelAPI import EveryPixelAPI
from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import get_attachments_from_attachments_or_fwd


class EstimatePhoto(CommonCommand):
    def __init__(self):
        names = ["оцени", "оценить"]
        help_text = "Оцени - оценить качество фотографии"
        detail_help_text = "Оцени (Изображение/Пересылаемое сообщение с изображением) - оценивает качество изображения"
        super().__init__(names, help_text, detail_help_text, api=False)

    def start(self):
        images = get_attachments_from_attachments_or_fwd(self.vk_event, 'photo')

        if not images:
            return "Не нашёл картинки"
        image = images[0]

        everypixel_api = EveryPixelAPI(image['download_url'])
        image_quality = everypixel_api.get_image_quality()
        return f"Качество картинки - {image_quality}"
