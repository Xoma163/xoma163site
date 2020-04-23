from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import decl_of_num, get_attachments_from_attachments_or_fwd
from apps.service.models import AudioList


class Audio(CommonCommand):
    def __init__(self):
        names = ["аудио", "плейлист"]
        help_text = "Аудио - сохраняет аудио в базу"
        detail_help_text = "Аудио [количество=5] - присылает рандомные треки \n" \
                           "Аудио (Прикреплённые аудио/Пересланное сообщение с аудио/Пересланное сообщение с постом " \
                           "в котором аудио) - сохраняет аудио в базу"
        super().__init__(names, help_text, detail_help_text, int_args=[0], api=False)

    def start(self):
        audios_att = get_attachments_from_attachments_or_fwd(self.vk_event, ['audio', 'wall'])
        if audios_att:
            self.save_attachments(audios_att)
            return "Добавил"
        else:
            count = 5
            if self.vk_event.args:
                count = self.vk_event.args[0]
                self.check_number_arg_range(count, 1, 10)
            # Fix issue with delete where limit
            audios = AudioList.objects.filter(
                pk__in=AudioList.objects.filter(author=self.vk_event.sender).order_by('?')[:count])
            if len(audios) == 0:
                return "Не нашёл ваших аудио"
            attachments = [audio.attachment for audio in audios]
            if len(audios) != count:
                msg = f"Нашёл только {len(audios)} {decl_of_num(len(audios), ['штуку', 'штуки', 'штук'])}"
            else:
                msg = "Лови"
            audios.delete()
            return {"msg": msg, "attachments": attachments}

    def save_attachments(self, attachments):
        for att in attachments:
            if att['type'] == 'audio':
                AudioList(author=self.vk_event.sender,
                          name=f"{att['artist']} - {att['title']}",
                          attachment=self.vk_bot.get_attachment_by_id('audio', att['owner_id'], att['id'])).save()

            elif att['type'] == 'wall':
                self.save_attachments(att['attachments'])
