import io
import json
import logging
import os
import threading
import traceback
from urllib.parse import urlparse

import requests
import urllib3
import vk_api
from django.contrib.auth.models import Group
from requests.exceptions import ReadTimeout, ConnectTimeout, SSLError
from vk_api import VkUpload
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id

from apps.API_VK.VkEvent import VkEvent
from apps.API_VK.VkUserClass import VkUserClass
from apps.API_VK.command.CommonMethods import check_user_group, get_user_groups, tanimoto
from apps.API_VK.command.Consts import Role
from apps.API_VK.command.commands.City import add_city_to_db
from apps.API_VK.command.commands.VoiceRecognition import have_audio_message
from apps.API_VK.models import VkUser, VkChat, VkBot
from apps.service.views import append_command_to_statistics
from secrets.secrets import secrets
from xoma163site.settings import TEST_CHAT_ID

logger = logging.getLogger('commands')


class VkBotClass(threading.Thread):

    def __init__(self):
        super().__init__()
        self._TOKEN = secrets['vk']['bot']['TOKEN']
        self.group_id = secrets['vk']['bot']['group_id']
        vk_session = vk_api.VkApi(token=self._TOKEN, api_version="5.107", config_filename="secrets/vk_bot_config.json")
        self.longpoll = MyVkBotLongPoll(vk_session, group_id=self.group_id)
        self.upload = VkUpload(vk_session)
        self.vk = vk_session.get_api()
        self.mentions = secrets['vk']['bot']['mentions']

        self.vk_user = VkUserClass()

        self.BOT_CAN_WORK = True
        self.DEBUG = False
        self.DEVELOP_DEBUG = False

    @staticmethod
    def parse_date(date):
        date_arr = date.split('.')
        if len(date_arr) == 2:
            return f"1970-{date_arr[1]}-{date_arr[0]}"
        else:
            return f"{date_arr[2]}-{date_arr[1]}-{date_arr[0]}"

    def need_a_response(self, vk_event, _have_audio_message, have_action):
        message = vk_event['message']['text']
        from_user = vk_event['from_user']

        if _have_audio_message:
            return True
        if have_action:
            return True
        if len(message) == 0:
            return False
        if from_user:
            return True
        if message[0] == '/':
            return True
        for mention in self.mentions:
            if message.find(mention) != -1:
                return True
        return False

    def set_activity(self, peer_id, activity='typing'):
        if activity not in ['typing', 'audiomessage']:
            raise RuntimeWarning("Не знаю такого типа активности")
        self.vk.messages.setActivity(type=activity, peer_id=peer_id, group_id=self.group_id)

    def send_message(self, peer_id, msg="ᅠ", attachments=None, keyboard=None, dont_parse_links=False, **kwargs):
        if attachments is None:
            attachments = []
        if isinstance(attachments, str):
            attachments = [attachments]
        if attachments and msg == "ᅠ":
            msg = ""
        if keyboard:
            keyboard = json.dumps(keyboard)
        msg = str(msg)
        if len(msg) > 4096:
            msg = msg[:4092]
            msg += "\n..."
        try:
            self.vk.messages.send(peer_id=peer_id,
                                  message=msg,
                                  access_token=self._TOKEN,
                                  random_id=get_random_id(),
                                  attachment=','.join(attachments),
                                  keyboard=keyboard,
                                  dont_parse_links=dont_parse_links
                                  )
        except vk_api.exceptions.ApiError as e:
            if e.code == 901:
                pass
            else:
                print("Ошибка отправки сообщения\n"
                      f"{e}")

    # Отправляет сообщения юзерам в разных потоках
    def parse_and_send_msgs_thread(self, chat_ids, message):
        if not isinstance(chat_ids, list):
            chat_ids = [chat_ids]
        for chat_id in chat_ids:
            thread = threading.Thread(target=self.parse_and_send_msgs, args=(chat_id, message,))
            thread.start()

    def parse_and_send_msgs(self, peer_id, result):
        if isinstance(result, str) or isinstance(result, int) or isinstance(result, float):
            result = {'msg': result}
        if isinstance(result, dict):
            result = [result]
        if isinstance(result, list):
            for msg in result:
                if isinstance(msg, str):
                    msg = {'msg': msg}
                if isinstance(msg, dict):
                    self.send_message(peer_id, **msg)

    def menu(self, vk_event, send=True):
        from apps.API_VK.command.initial import get_commands

        # Проверяем не остановлен ли бот, если так, то проверяем вводимая команда = старт?
        if not self.check_bot_working():
            if not check_user_group(vk_event.sender, Role.ADMIN):
                return

            if vk_event.command in ['старт']:
                self.BOT_CAN_WORK = True
                # cameraHandler.resume()
                msg = "Стартуем!"
                self.send_message(vk_event.peer_id, msg)
                log_result = {'result': msg}
                logger.debug(log_result)
                return msg
            return

        group = vk_event.sender.groups.filter(name=Role.BANNED.name)
        if len(group) > 0:
            return

        if self.DEBUG and send:
            if hasattr(vk_event, 'payload') and vk_event.payload:
                debug_message = \
                    f"msg = {vk_event.msg}\n" \
                    f"command = {vk_event.command}\n" \
                    f"args = {vk_event.args}\n" \
                    f"payload = {vk_event.payload}\n"
            else:
                debug_message = \
                    f"msg = {vk_event.msg}\n" \
                    f"command = {vk_event.command}\n" \
                    f"args = {vk_event.args}\n" \
                    f"original_args = {vk_event.original_args}\n"
            self.send_message(vk_event.peer_id, debug_message)

        log_vk_event = {'vk_event': vk_event}
        logger.debug(log_vk_event)

        commands = get_commands()
        for command in commands:
            try:
                if command.accept(vk_event):
                    result = command.__class__().check_and_start(self, vk_event)
                    if send:
                        self.parse_and_send_msgs(vk_event.peer_id, result)
                    append_command_to_statistics(vk_event.command)
                    log_result = {'result': result}
                    logger.debug(log_result)
                    return result
            except RuntimeWarning as e:
                msg = str(e)
                log_runtime_warning = {'result': msg}
                logger.warning(log_runtime_warning)

                if send:
                    self.parse_and_send_msgs(vk_event.peer_id, msg)
                return msg
            except RuntimeError as e:
                exception = str(e)
                log_runtime_error = {'exception': exception, 'result': exception}
                logger.error(log_runtime_error)
                if send:
                    self.parse_and_send_msgs(vk_event.peer_id, exception)
                return exception
            except Exception as e:
                msg = "Непредвиденная ошибка. Сообщите разработчику в группе или команда /баг"
                tb = traceback.format_exc()
                log_exception = {
                    'exception': str(e),
                    'result': msg
                }
                logger.error(log_exception, exc_info=tb)
                if send:
                    self.parse_and_send_msgs(vk_event.peer_id, msg)
                return msg

        if vk_event.chat and not vk_event.chat.need_reaction:
            return None
        similar_command = commands[0].names[0]
        tanimoto_max = 0
        user_groups = get_user_groups(vk_event.sender)
        for command in commands:
            # Выдача пользователю только тех команд, которые ему доступны
            command_access = command.access
            if isinstance(command_access, str):
                command_access = [command_access]
            if command_access.name not in user_groups:
                continue

            for name in command.names:
                if name:
                    tanimoto_current = tanimoto(vk_event.command, name)
                    if tanimoto_current > tanimoto_max:
                        tanimoto_max = tanimoto_current
                        similar_command = name

        msg = f"Я не понял команды \"{vk_event.command}\"\n"
        if tanimoto_max != 0:
            msg += f"Возможно вы имели в виду команду \"{similar_command}\""
        logger_result = {'result': msg}
        logger.debug(logger_result)
        if send:
            self.send_message(vk_event.peer_id, msg)
        return msg

    def listen_longpoll(self):
        for event in self.longpoll.listen():
            try:
                # Если пришло новое сообщение
                if event.type == VkBotEventType.MESSAGE_NEW:

                    # from_user - сообщение пришло из диалога с пользователем
                    # chat_id - присутствует только в чатах
                    # text - текст сообщения
                    # from_id - кто отправил сообщение (если значение отрицательное, то другой бот)
                    # user_id - id пользователя
                    # peer_id - откуда отправил сообщение (если там значение совпадает с from_id, то это from_user,
                    # если нет и значение начинается на 200000000*, то это конфа
                    # payload - скрытая информация, которая передаётся при нажатии на кнопку

                    vk_event = {
                        'from_user': event.from_user,
                        'chat_id': event.chat_id,
                        'user_id': event.message.from_id,
                        'peer_id': event.message.peer_id,
                        'message': {
                            # 'id': event.message.id,
                            'text': event.message.text,
                            'payload': event.message.payload,
                            'attachments': event.message.attachments,
                            'action': event.message.action
                        },
                        'fwd': None
                    }
                    # Если я запустился из под дебага, реагируй только на меня и только в моей конфе
                    if self.DEVELOP_DEBUG:
                        from_test_chat = vk_event['chat_id'] == TEST_CHAT_ID
                        from_me = str(vk_event['user_id']) == secrets['vk']['admin_id']
                        if not from_test_chat or not from_me:
                            continue

                    # Обработка вложенных сообщений в vk_event['fwd']. reply и fwd для вк это разные вещи.
                    if event.message.reply_message:
                        vk_event['fwd'] = [event.message.reply_message]
                    elif len(event.message.fwd_messages) != 0:
                        vk_event['fwd'] = event.message.fwd_messages

                    # Проверка есть ли аудиосообщения
                    have_audio_message_flag = have_audio_message(vk_event)

                    # Проверка есть ли в сообщении action
                    have_action = vk_event['message']['action'] is not None

                    # Сообщение либо мне в лс, либо упоминание меня, либо есть аудиосообщение, либо есть экшн
                    if not self.need_a_response(vk_event, have_audio_message_flag, have_action):
                        continue

                    # Узнаём пользователя
                    if vk_event['user_id'] > 0:
                        vk_event['sender'] = self.get_user_by_id(vk_event['user_id'])
                    else:
                        self.send_message(vk_event['peer_id'], "Боты не могут общаться с Петровичем :(")
                        continue

                    # Узнаём конфу
                    if vk_event['chat_id']:
                        vk_event['chat'] = self.get_chat_by_id(int(vk_event['peer_id']))
                        if vk_event['sender'] and vk_event['chat']:
                            self.add_group_to_user(vk_event['sender'], vk_event['chat'])
                    else:
                        vk_event['chat'] = None

                    vk_event_object = VkEvent(vk_event)
                    thread = threading.Thread(target=self.menu, args=(vk_event_object,))
                    thread.start()
                else:
                    pass

            except Exception as e:
                tb = traceback.format_exc()
                log_exception = {
                    'exception': str(e),
                }
                logger.error(log_exception, exc_info=tb)

    def run(self):
        self.listen_longpoll()

    def get_chat_title(self, chat_id):
        return self.vk.messages.getconversationById(peer_ids=2000000000 + chat_id)['items'][0]['chat_settings'][
            'title']

    def set_chat_title(self, chat_id, title):
        self.vk.messages.editChat(chat_id=chat_id, title=title)

    def set_chat_title_if_not_equals(self, chat_id, title):
        if title != self.vk.messages.getconversationById(peer_ids=2000000000 + chat_id)['items'][0]['chat_settings'][
            'title']:
            self.vk.messages.editChat(chat_id=chat_id, title=title)

    def get_user_by_id(self, user_id):
        vk_user = VkUser.objects.filter(user_id=user_id)
        if len(vk_user) > 0:
            vk_user = vk_user.first()
        else:
            # Прозрачная регистрация
            user = self.vk.users.get(user_id=user_id, lang='ru', fields='sex, bdate, city, screen_name')[0]
            vk_user = VkUser()
            vk_user.user_id = user_id
            vk_user.name = user['first_name']
            vk_user.surname = user['last_name']
            if 'sex' in user:
                vk_user.gender = user['sex']
            if 'bdate' in user:
                vk_user.birthday = self.parse_date(user['bdate'])
            if 'city' in user:
                from apps.service.models import City
                city_name = user['city']['title']
                city = City.objects.filter(name=city_name)
                if len(city) > 0:
                    city = city.first()
                else:
                    try:
                        city = add_city_to_db(city_name)
                    except Exception:
                        city = None
                vk_user.city = city
            else:
                vk_user.city = None
            if 'screen_name' in user:
                vk_user.nickname = user['screen_name']
            vk_user.save()
            group_user = Group.objects.get(name=Role.USER.name)
            vk_user.groups.add(group_user)
            vk_user.save()
        return vk_user

    @staticmethod
    def get_gamer_by_user(user):
        from apps.games.models import Gamer

        gamers = Gamer.objects.filter(user=user)
        if len(gamers) == 0:
            gamer = Gamer(user=user)
            gamer.save()
            return gamer
        elif len(gamers) > 1:
            raise RuntimeWarning("Два и более игрока подходит под поиск")
        else:
            return gamers.first()

    @staticmethod
    def get_user_by_name(args, filter_chat=None):
        if not args:
            raise RuntimeWarning("Отсутствуют аргументы")
        if isinstance(args, str):
            args = [args]
        vk_users = VkUser.objects
        if filter_chat:
            vk_users = vk_users.filter(chats=filter_chat)
        if len(args) >= 2:
            user = vk_users.filter(name=args[0].capitalize(), surname=args[1].capitalize())
        else:
            user = vk_users.filter(nickname_real=args[0].capitalize())
            if len(user) == 0:
                user = vk_users.filter(name=args[0].capitalize())
                if len(user) == 0:
                    user = vk_users.filter(surname=args[0].capitalize())
                    if len(user) == 0:
                        user = vk_users.filter(nickname=args[0])
                        if len(user) == 0:
                            user = vk_users.filter(user_id=args[0])

        if len(user) > 1:
            raise RuntimeWarning("2 и более пользователей подходит под поиск")

        if len(user) == 0:
            raise RuntimeWarning("Пользователь не найден. Возможно опечатка или он мне ещё ни разу не писал")

        return user.first()

    @staticmethod
    def get_chat_by_name(args):
        if not args:
            raise RuntimeWarning("Отсутствуют аргументы")
        if isinstance(args, str):
            args = [args]
        vk_chats = VkChat.objects
        for arg in args:
            vk_chats = vk_chats.filter(name__icontains=arg)

        if len(vk_chats) > 1:
            raise RuntimeWarning("2 и более чатов подходит под поиск")

        if len(vk_chats) == 0:
            raise RuntimeWarning("Чат не найден")
        return vk_chats.first()

    def get_bot_by_id(self, bot_id):
        if bot_id > 0:
            bot_id -= 1
        vk_bot = VkBot.objects.filter(bot_id=bot_id)
        if len(vk_bot) > 0:
            vk_bot = vk_bot.first()
        else:
            # Прозрачная регистрация
            bot = self.vk.groups.getById(group_id=bot_id)[0]

            vk_bot = VkBot()
            vk_bot.bot_id = bot_id
            vk_bot.name = bot['name']
            vk_bot.save()

        return vk_bot

    @staticmethod
    def get_chat_by_id(chat_id):
        vk_chat = VkChat.objects.filter(chat_id=chat_id)
        if len(vk_chat) > 0:
            vk_chat = vk_chat.first()
        else:
            vk_chat = VkChat(chat_id=chat_id)
            vk_chat.save()
        return vk_chat

    @staticmethod
    def add_group_to_user(vk_user, chat):
        chats = vk_user.chats
        if chat not in chats.all():
            chats.add(chat)

    @staticmethod
    def remove_group_from_user(vk_user, chat):
        chats = vk_user.chats
        if chat in chats.all():
            chats.remove(chat)

    @staticmethod
    def get_group_id(_id):
        return 2000000000 + int(_id)

    def get_short_link(self, long_link):
        result = self.vk.utils.getShortLink(url=long_link)
        if 'short_url' in result:
            return result['short_url']
        else:
            return None

    def check_bot_working(self):
        return self.BOT_CAN_WORK

    @staticmethod
    def _prepare_obj_to_upload(file_like_object, allowed_exts_url=None):
        # bytes array
        if isinstance(file_like_object, bytes):
            obj = io.BytesIO(file_like_object)
            obj.seek(0)
        # bytesIO
        elif isinstance(file_like_object, io.BytesIO):
            obj = file_like_object
            obj.seek(0)
        # url
        elif urlparse(file_like_object).hostname:
            if allowed_exts_url:
                if file_like_object.split('.')[-1].lower() not in allowed_exts_url:
                    raise RuntimeWarning(f"Загрузка по URL доступна только для {' '.join(allowed_exts_url)}")
            try:
                response = requests.get(file_like_object, stream=True, timeout=3)
            except SSLError:
                raise RuntimeWarning(f"SSLError")
            except requests.exceptions.ConnectionError:
                raise RuntimeWarning(f"ConnectionError")
            obj = response.raw
        # path
        else:
            obj = file_like_object
        return obj

    def upload_photos(self, images, max_count=10):
        if not isinstance(images, list):
            images = [images]

        attachments = []
        images_to_load = []
        for image in images:
            try:
                image = self._prepare_obj_to_upload(image, ['jpg', 'jpeg', 'png'])
            except RuntimeWarning:
                continue
            except ReadTimeout:
                continue
            except ConnectTimeout:
                continue
            # Если Content-Length > 50mb
            bytes_count = None
            if isinstance(image, io.BytesIO):
                bytes_count = image.getbuffer().nbytes
            elif isinstance(image, urllib3.response.HTTPResponse) or isinstance(image,
                                                                                requests.packages.urllib3.response.HTTPResponse):
                bytes_count = image.headers.get('Content-Length')
            elif os.path.exists(image):
                bytes_count = os.path.getsize(image)
            else:
                print("ШТО ТЫ ТАКОЕ", type(image))
            if not bytes_count:
                continue
            if int(bytes_count) / 1024 / 1024 > 50:
                continue
            images_to_load.append(image)

            if len(images_to_load) >= max_count:
                break
        try:
            vk_photos = self.upload.photo_messages(images_to_load)
            for vk_photo in vk_photos:
                attachments.append(self.get_attachment_by_id('photo', vk_photo['owner_id'], vk_photo['id']))
        except vk_api.exceptions.ApiError as e:
            print(e)
        return attachments

    def upload_document(self, document, peer_id, title='Документ'):
        document = self._prepare_obj_to_upload(document)
        vk_document = self.upload.document_message(document, title=title, peer_id=peer_id)['doc']
        return self.get_attachment_by_id('doc', vk_document['owner_id'], vk_document['id'])

    def upload_audio(self, audio, artist, title):
        audio = self._prepare_obj_to_upload(audio)
        try:
            vk_audio = self.vk_user.upload.audio(audio, artist=artist, title=title)
        except vk_api.exceptions.ApiError as e:
            if e.code == 270:
                raise RuntimeError("Аудиозапись была удалена по просьбе правообладателя")
            raise RuntimeError("Ошибка загрузки аудиозаписи")
        return self.get_attachment_by_id('audio', vk_audio['owner_id'], vk_audio['id'])

    def upload_video_by_link(self, link, name):
        values = {
            'name': name,
            'is_private': True,
            'link': link,
        }

        response = self.vk_user.vk.video.save(**values)
        response2 = requests.post(response['upload_url']).json()
        print(response2)

        return f"video{response['owner_id']}_{response['video_id']}"

    def get_attachment_by_id(self, _type, group_id, _id):
        if group_id is None:
            group_id = f'-{self.group_id}'
        return f"{_type}{group_id}_{_id}"


class MyVkBotLongPoll(VkBotLongPoll):
    def listen(self):
        while True:
            try:
                for event in self.check():
                    yield event
            except Exception as e:
                error = {'exception': f'Longpoll Error (VK): {str(e)}'}
                logger.error(error)
