import json
from datetime import datetime

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import normalize_datetime, get_attachments_for_upload
from apps.service.models import LaterMessage


class Discord(CommonCommand):
    def __init__(self):
        names = ["потом"]
        help_text = "Потом - добавляет сообщения и вложения из пересланных сообщений, чтобы посмотреть потом."
        detail_help_text = "Потом (пересланные сообщения) - добавляет сообщения и вложения из пересланных сообщений, " \
                           "чтобы посмотреть потом.\n" \
                           "Потом - присылает одно случайное вложение"
        super().__init__(names, help_text, detail_help_text)

    def start(self):
        from apps.API_VK.VkBotClass import parse_attachments
        if self.vk_event.fwd:
            for fwd in self.vk_event.fwd:
                attachments = parse_attachments(fwd['attachments'])
                new_lm = {'author': self.vk_event.sender,
                          'text': fwd['text'],
                          'date': normalize_datetime(datetime.fromtimestamp(fwd['date']), "UTC"),
                          'attachments': json.dumps(attachments)
                          }
                if fwd['from_id'] > 0:
                    new_lm['message_author'] = self.vk_bot.get_user_by_id(fwd['from_id'])
                else:
                    new_lm['message_bot'] = self.vk_bot.get_bot_by_id(fwd['from_id'])
                lm = LaterMessage(**new_lm)
                lm.save()
            return "Сохранил"
        else:
            lm = LaterMessage.objects.filter(author=self.vk_event.sender).order_by('?').first()
            if not lm:
                return "Ничего не нашёл :("
            else:
                msg = f"{lm.message_author} ({lm.date.strftime('%d.%m.%Y %H:%M:%S')}):\n" \
                      f"{lm.text}"
                attachments = []
                if lm.attachments:
                    lm_attachments = json.loads(lm.attachments)
                    attachments = get_attachments_for_upload(self.vk_bot, lm_attachments)
                lm.delete()
                return {"msg": msg, "attachments": attachments}
