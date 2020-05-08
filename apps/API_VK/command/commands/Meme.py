from apps.API_VK.command import Role
from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import get_inline_keyboard, get_attachments_from_attachments_or_fwd, \
    check_user_group, get_one_chat_with_user

from apps.service.models import Meme as MemeModel
from xoma163site.settings import VK_URL, TEST_CHAT_ID

IMAGE_EXTS = ['jpg', 'jpeg', 'png']


def check_name_exists(name):
    return MemeModel.objects.filter(name=name).exists()


class Meme(CommonCommand):
    def __init__(self):
        names = ["мем"]
        help_text = "Мем - присылает нужный мем"
        detail_help_text = "Мем (название) - присылает нужный мем\n" \
                           "Мем р - присылает рандомный мем\n" \
                           "Мем добавить (Вложение/Пересланное сообщение с вложением) (название) - добавляет мем. \n" \
                           "Мем обновить (Вложение/Пересланное сообщение с вложением) (название) - обновляет созданный вами мем. \n" \
                           "Можно добавлять картинки/гифки/аудио/видео\n" \
                           "Мем удалить (название) - удаляет созданный вами мем\n" \
                           "Мем конфа (название конфы) (название/рандом) - отправляет мем в конфу\n\n" \
                           "Для модераторов:\n" \
                           "Мем подтвердить - присылает мем на подтверждение\n" \
                           "Мем подтвердить (id) - подтверждает мем\n" \
                           "Мем отклонить (id) [причина] - отклоняет мем\n" \
                           "Мем удалить (название) - удаляет мем"
        super().__init__(names, help_text, detail_help_text, args=1)

    def start(self):
        if self.vk_event.args[0] in ['добавить']:
            self.check_args(2)
            attachments = get_attachments_from_attachments_or_fwd(self.vk_event, ['audio', 'video', 'photo', 'doc'])
            if len(attachments) == 0:
                return "Не нашёл вложений в сообщении или пересланном сообщении"
            attachment = attachments[0]

            for i, _ in enumerate(self.vk_event.args):
                self.vk_event.args[i] = self.vk_event.args[i].lower()

            new_meme = {
                'name': " ".join(self.vk_event.args[1:]),
                'type': attachment['type'],
                'author': self.vk_event.sender,
                'approved': check_user_group(self.vk_event.sender, Role.MODERATOR.name) or check_user_group(
                    self.vk_event.sender, Role.TRUSTED.name)
            }

            if MemeModel.objects.filter(name=new_meme['name']).exists():
                return "Мем с таким названием уже есть в базе"

            if attachment['type'] == 'video' or attachment['type'] == 'audio':
                new_meme['link'] = attachment['url']
            elif attachment['type'] == 'photo' or attachment['type'] == 'doc':
                new_meme['link'] = attachment['download_url']
            else:
                return "Невозможно"

            new_meme_obj = MemeModel.objects.create(**new_meme)
            if new_meme['approved']:
                return "Добавил"
            else:
                meme_to_send = self.prepare_meme_to_send(new_meme_obj)
                meme_to_send['msg'] = "Запрос на подтверждение мема:\n" \
                                      f"{new_meme_obj.author}\n" \
                                      f"{new_meme_obj.name} ({new_meme_obj.id})"
                self.vk_bot.parse_and_send_msgs(self.vk_bot.get_group_id(TEST_CHAT_ID), meme_to_send)
                return "Добавил. Воспользоваться мемом можно после проверки модераторами."
        elif self.vk_event.args[0] in ['обновить']:
            self.check_args(2)
            attachments = get_attachments_from_attachments_or_fwd(self.vk_event, ['audio', 'video', 'photo', 'doc'])
            if len(attachments) == 0:
                return "Не нашёл вложений в сообщении или пересланном сообщении"
            attachment = attachments[0]
            if attachment['type'] == 'video' or attachment['type'] == 'audio':
                new_meme_link = attachment['url']
            elif attachment['type'] == 'photo' or attachment['type'] == 'doc':
                new_meme_link = attachment['download_url']
            else:
                return "Невозможно"

            if check_user_group(self.vk_event.sender, Role.MODERATOR.name) or check_user_group(self.vk_event.sender,
                                                                                               Role.TRUSTED.name):
                meme = self.get_meme(self.vk_event.args[1:])
                meme.link = new_meme_link
                meme.type = attachment['type']
                meme.save()
                return f'Обновил мем "{meme.name}"'
            else:
                meme = self.get_meme(self.vk_event.args[1:], self.vk_event.sender)
                meme.link = new_meme_link
                meme.approved = False
                meme.type = attachment['type']
                meme.save()

                meme_to_send = self.prepare_meme_to_send(meme)
                meme_to_send['msg'] = "Запрос на обновление мема:\n" \
                                      f"{meme.author}\n" \
                                      f"{meme.name} ({meme.id})"
                self.vk_bot.parse_and_send_msgs(self.vk_bot.get_group_id(TEST_CHAT_ID), meme_to_send)
                return "Обновил. Воспользоваться мемом можно после проверки модераторами."


        elif self.vk_event.args[0] in ['удалить']:
            self.check_args(2)
            if check_user_group(self.vk_event.sender, Role.MODERATOR.name):
                meme = self.get_meme(self.vk_event.args[1:])
                self.vk_bot.send_message(meme.author.user_id, f'Мем с названием "{meme.name}" удалён поскольку он не '
                                                              f'соответствует правилам.')
            else:
                meme = self.get_meme(self.vk_event.args[1:], self.vk_event.sender)
            meme_name = meme.name
            meme.delete()
            return f'Удалил мем "{meme_name}"'
        elif self.vk_event.args[0] in ['конфа']:
            self.check_args(3)
            chat = get_one_chat_with_user(self.vk_event.args[1], self.vk_event.sender.user_id)
            if self.vk_event.args[-1] in ['рандом', 'р']:
                meme = self.get_random_meme()
            else:
                meme = self.get_meme(self.vk_event.args[2:])
            prepared_meme = self.prepare_meme_to_send(meme, print_name=True)
            self.vk_bot.parse_and_send_msgs(chat.chat_id, prepared_meme)
            return "Отправил"
        elif self.vk_event.args[0] in ['р', 'рандом']:
            meme = self.get_random_meme()
            return self.prepare_meme_to_send(meme, print_name=True, send_keyboard=True)
        elif self.vk_event.args[0] in ['подтвердить', 'принять', '+']:
            self.check_sender(Role.MODERATOR.name)
            if len(self.vk_event.args) == 1:
                meme = self.get_meme(approved=False)
                meme_to_send = self.prepare_meme_to_send(meme)
                meme_to_send['msg'] = f"{meme.author}\n" \
                                      f"{meme.name} ({meme.id})"
                return meme_to_send
            else:
                self.int_args = [1]
                self.parse_int()
                non_approved_meme = MemeModel.objects.filter(id=self.vk_event.args[1]).first()
                if not non_approved_meme:
                    return "Не нашёл мема с таким id"
                if non_approved_meme.approved:
                    return "Мем уже подтверждён"

                user_msg = f'Мем с названием "{non_approved_meme.name}" подтверждён.'
                self.vk_bot.send_message(non_approved_meme.author.user_id, user_msg)

                msg = f'Мем "{non_approved_meme.name}" ({non_approved_meme.id}) подтверждён'
                non_approved_meme.approved = True
                non_approved_meme.save()
                return msg
        elif self.vk_event.args[0] in ['отклонить', '-']:
            self.check_sender(Role.MODERATOR.name)
            self.int_args = [1]
            self.parse_int()
            non_approved_meme = MemeModel.objects.filter(id=self.vk_event.args[1]).first()
            if not non_approved_meme:
                return "Не нашёл мема с таким id"
            if non_approved_meme.approved:
                return "Мем уже подтверждён"

            reason = None
            if len(self.vk_event.args) > 2:
                reason = " ".join(self.vk_event.args[2:])
            user_msg = f'Мем с названием "{non_approved_meme.name}" отклонён.'
            if reason:
                user_msg += f"\nПричина: {reason}"
            self.vk_bot.send_message(non_approved_meme.author.user_id, user_msg)

            msg = f'Мем "{non_approved_meme.name}" ({non_approved_meme.id}) отклонён'
            non_approved_meme.delete()
            return msg
        else:
            meme = self.get_meme(self.vk_event.args)
            meme.uses += 1
            meme.save()
            return self.prepare_meme_to_send(meme)

    @staticmethod
    def get_meme(filter_list=None, filter_user=None, approved=True):
        memes = MemeModel.objects.filter(approved=approved)

        if filter_list:
            for _filter in filter_list:
                memes = memes.filter(name__icontains=_filter)

        if filter_user:
            memes = memes.filter(author=filter_user)

        if len(memes) == 0:
            raise RuntimeError("Не нашёл :(")
        elif len(memes) == 1:
            return memes.first()
        else:
            for meme in memes:
                if meme.name == " ".join(filter_list):
                    return meme
            memes = memes[:10]
            meme_names = [meme.name for meme in memes]
            meme_names_str = ";\n".join(meme_names)

            msg = f"Нашёл сразу {len(memes)}, уточните:\n\n" \
                  f"{meme_names_str}" + '.'
            if len(memes) > 10:
                msg += f"\n..."
            raise RuntimeWarning(msg)

    @staticmethod
    def get_random_meme():
        return MemeModel.objects.order_by('?').first()

    def prepare_meme_to_send(self, meme, print_name=False, send_keyboard=False):
        msg = {}
        if meme.type == 'video' or meme.type == 'audio':
            msg['attachments'] = [meme.link.replace(VK_URL, '')]
        elif meme.type == 'photo':
            msg['attachments'] = self.vk_bot.upload_photos(meme.link)
        elif meme.type == 'doc':
            msg['attachments'] = self.vk_bot.upload_document(meme.link, self.vk_event.peer_id)
        else:
            raise RuntimeError("У мема нет типа. Тыкай разраба")

        if print_name:
            msg['msg'] = meme.name

        if send_keyboard:
            msg['keyboard'] = get_inline_keyboard(self.names[0], args={"random": "р"})
        return msg
