import json
from datetime import datetime

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import normalize_datetime, get_attachments_for_upload
from apps.service.models import LaterMessage


class Discord(CommonCommand):
    def __init__(self):
        names = ["потом"]
        help_text = "Потом - добавляет сообщения и вложения из пересланных сообщений, чтобы посмотреть потом"
        detail_help_text = "Потом (Пересланные сообщения) - добавляет сообщения и вложения из пересланных сообщений, " \
                           "чтобы посмотреть потом\n" \
                           "Потом - присылает последнее сохранённое сообщение и удалет его из базы"
        super().__init__(names, help_text, detail_help_text)

    def start(self):
        if self.vk_event.fwd:
            for fwd in self.vk_event.fwd:
                lm = LaterMessage(
                    author=self.vk_event.sender,
                    text=fwd['text'],
                    date=normalize_datetime(
                        datetime.fromtimestamp(fwd['date']), "UTC"))

                if fwd['from_id'] > 0:
                    lm.message_author = self.vk_bot.get_user_by_id(fwd['from_id'])
                else:
                    lm.message_bot = self.vk_bot.get_bot_by_id(fwd['from_id'])

                attachments = self.vk_event.parse_attachments(fwd['attachments'])
                if attachments:
                    lm.attachments = json.dumps(attachments)
                lm.save()
            return "Сохранил"
        else:
            lm = LaterMessage.objects.filter(author=self.vk_event.sender).order_by('date').first()
            if not lm:
                return "Ничего не нашёл :("
            else:

                author = None
                if lm.message_author:
                    author = lm.message_author
                elif lm.message_bot:
                    author = lm.message_bot

                msg = f"{author} ({lm.date.strftime('%d.%m.%Y %H:%M:%S')}):\n" \
                      f"{lm.text}"
                attachments = []
                if lm.attachments and lm.attachments != "null":
                    lm_attachments = json.loads(lm.attachments)
                    attachments = get_attachments_for_upload(self.vk_bot, lm_attachments)
                lm.delete()
                return {"msg": msg, "attachments": attachments}
