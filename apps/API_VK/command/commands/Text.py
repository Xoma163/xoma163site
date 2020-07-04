from apps.API_VK.APIs.OCR import OCRApi
from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import get_attachments_from_attachments_or_fwd


class Statistics(CommonCommand):
    def __init__(self):
        names = ["текст"]
        help_text = "Текст - распознаёт текст на изображении"
        detail_help_text = "Текст (Изображения/Пересылаемое сообщение с изображением) [язык=rus] - распознаёт текст на изображении\n" \
                           'Язык нужно указывать в 3 символа. Пример - "eng", "rus", "fre", "ger" и так далее'
        super().__init__(names, help_text, detail_help_text, api=False)

    def start(self):
        lang = "rus"
        if self.vk_event.args:
            lang = self.vk_event.args[0]

        google_ocr = OCRApi()
        images = get_attachments_from_attachments_or_fwd(self.vk_event, 'photo')
        if not images:
            return "Не нашёл картинки"
        image = images[0]
        return google_ocr.recognize(image['download_url'], lang)
