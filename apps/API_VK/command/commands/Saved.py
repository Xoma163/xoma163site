from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import get_attachments_from_attachments_or_fwd


class Saved(CommonCommand):
    def __init__(self):
        names = ["сохраненка", "перешли", "сохраненные"]
        help_text = "Сохранёнка (фотографии) - пересылает фотографии, чтобы их можно было сохранить в вк в сохранёнки"
        super().__init__(names, help_text, api=False)

    def start(self):
        attachments = get_attachments_from_attachments_or_fwd(self.vk_event, 'photo')
        if len(attachments) == 0:
            return "Не нашёл в сообщении фотографий"
        attachments_vk_url = [attachment['download_url'] for attachment in attachments]
        attachments = self.vk_bot.upload_photos(attachments_vk_url)
        return {'attachments': attachments}
