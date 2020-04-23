from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import get_inline_keyboard, get_attachments_from_attachments_or_fwd

from apps.service.models import Meme as MemeModel

IMAGE_EXTS = ['jpg', 'jpeg', 'png']


def check_name_exists(name):
    return MemeModel.objects.filter(name=name).exists()


class Meme(CommonCommand):
    def __init__(self):
        names = ["мем"]
        help_text = "Мем - присылает нужный мем"
        detail_help_text = "Мем (название) - присылает нужный мем\n" \
                           "Мем р - присылает рандомный мем\n" \
                           "Добавление мема - /мем добавить ...(название) (url)\n" \
                           "Добавление мема - /мем добавить (Вложение/Пересланное сообщение с вложением) (название)\n" \
                           "Отправка мема в конфу - /мем конфа (название конфы) (название/рандом)\n"
        super().__init__(names, help_text, detail_help_text, args=1)

    def get_1_meme(self, filter_list):
        memes = MemeModel.objects.all()

        for _filter in filter_list:
            memes = memes.filter(name__icontains=_filter)
        if len(memes) == 0:
            raise RuntimeError("Не нашёл :(")
        elif len(memes) == 1:
            return memes.first()
        else:
            for meme in memes:
                if meme.name == self.vk_event.original_args:
                    # if check_name_exists(self.vk_event.original_args):
                    return meme
            memes10 = memes[:10]
            meme_names = [meme.name for meme in memes10]
            meme_names_str = ";\n".join(meme_names)

            msg = f"Нашёл сразу несколько, уточните:\n\n" \
                  f"{meme_names_str}" + '.'
            if len(memes) > 10:
                msg += "\n..."
            raise RuntimeError(msg)

    def send_1_meme_to_chat(self, meme, chat, print_name=True):
        meme = self.send_1_meme(meme, print_name)
        if type(meme) == dict:
            self.vk_bot.parse_and_send_msgs(chat.chat_id, meme)
            return "Отправил"
        else:
            return "Не нашёл мем :("

    def send_1_meme(self, meme, print_name=True, send_keyboard=False):
        meme_name = ""
        if print_name:
            meme_name = meme.name

        if meme.link:
            msg = {'msg': meme.link}
            allowed_attachments = ['video', 'audio']
            for allowed_attachment in allowed_attachments:
                if meme.link.find('vk.com') != -1 and meme.link.find(allowed_attachment) != -1:
                    attachment = meme.link[meme.link.find(allowed_attachment):]
                    msg = {'msg': meme_name, 'attachments': [attachment]}
                    break
        elif meme.image:
            if meme.image.name.split('.')[-1] == 'gif':
                attachment = self.vk_bot.upload_document(meme.image.path, self.vk_event.peer_id, False)
            else:
                attachment = self.vk_bot.upload_photo(meme.image.path)
            msg = {'msg': meme_name, 'attachments': [attachment]}
        else:
            return "Какая-то хрень с мемом"
        if send_keyboard:
            msg['keyboard'] = get_inline_keyboard(self.names[0], args={"random": "р"})
        return msg

    def start(self):
        from apps.API_VK.command.CommonMethods import get_one_chat_with_user

        for i in range(len(self.vk_event.args)):
            self.vk_event.args[i] = self.vk_event.args[i].lower()
        self.vk_event.original_args = self.vk_event.original_args.lower()

        if self.vk_event.args[0] == 'добавить':
            self.check_args(2)

            if self.vk_event.attachments or self.vk_event.fwd:
                new_meme = {'name': self.vk_event.original_args.split(' ', 1)[1], 'author': self.vk_event.sender}
                if check_name_exists(new_meme['name']):
                    return "Мем с таким названием уже есть"
                attachments = get_attachments_from_attachments_or_fwd(self.vk_event, ['photo', 'audio', 'video', 'doc'])
                if len(attachments) == 0:
                    return "Не нашёл вложений в сообщении или пересланных сообщениях"
                attachment = attachments[0]
                if attachment['type'] == 'photo':
                    meme = MemeModel(**new_meme)
                    meme.save()
                    meme.save_remote_image(attachment['download_url'])
                elif attachment['type'] == 'video' or attachment['type'] == 'audio':
                    new_meme['link'] = attachment['url']
                    meme = MemeModel(**new_meme)
                    meme.save()
                elif attachment['type'] == 'doc':
                    allowed_type = 'gif'
                    if attachment['ext'] != allowed_type:
                        return "Вложение должно быть типа gif"
                    meme = MemeModel(**new_meme)
                    meme.save()
                    meme.save_remote_image(attachment['download_url'], allowed_type)
                else:
                    return "Не знаю такого типа вложения"
                return "Сохранил"
            elif len(self.vk_event.args) >= 3:
                new_meme = {'link': self.vk_event.args[-1], 'author': self.vk_event.sender}
                name = self.vk_event.original_args.split(' ', 1)[1]
                new_meme['name'] = name[:name.rfind(new_meme['link']) - 1]
                if check_name_exists(new_meme['name']):
                    return "Мем с таким названием уже есть"
                for meme_ext in IMAGE_EXTS:
                    # Если урл - картинка
                    if new_meme['link'].split('.')[-1].lower() == meme_ext:
                        link = new_meme.pop('link')
                        meme = MemeModel(**new_meme)
                        meme.save()
                        meme.save_remote_image(link)
                        return "Сохранил"

                MemeModel(**new_meme).save()
                return "Сохранил"
            else:
                return "Не передан url видео или не прикреплена картинка"
        elif self.vk_event.args[0] in ['рандом', 'р']:
            meme = MemeModel.objects.all().order_by('?').first()
            return self.send_1_meme(meme, send_keyboard=True)
        elif self.vk_event.args[0] in ['конфа', 'конференция', 'чат']:

            self.check_args(3)
            if self.vk_event.args[-1] in ['рандом', 'р']:
                meme = MemeModel.objects.all().order_by('?').first()
            else:
                meme_name_filter = self.vk_event.args[2:]
                meme = self.get_1_meme(meme_name_filter)
            chat = get_one_chat_with_user(self.vk_event.args[1], self.vk_event.sender.user_id)

            return self.send_1_meme_to_chat(meme, chat, False)

        else:
            meme = self.get_1_meme(self.vk_event.args)
            return self.send_1_meme(meme, False)
