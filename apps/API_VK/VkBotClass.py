import io
import json
import logging
import re
import threading
import traceback
from urllib.parse import urlparse

import requests
import vk_api
from django.contrib.auth.models import Group
from vk_api import VkUpload
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id

from apps.API_VK.VkEvent import VkEvent
from apps.API_VK.command import get_commands
from apps.API_VK.command.CommonMethods import check_user_group
from apps.API_VK.models import VkUser, VkChat, VkBot
from apps.service.views import append_command_to_statistics
from secrets.secrets import secrets

logger = logging.getLogger('commands')


def parse_msg_to_me(msg, mentions):
    # Обрезаем палку
    if msg[0] == '/':
        msg = msg[1:]
    for mention in mentions:
        msg = msg.replace(mention, '')
    return msg


def parse_msg(msg):
    # Сообщение, команда, аргументы, аргументы строкой, ключи
    """
    msg - оригинальное сообщение
    command - команда
    args - список аргументов
    original_args - строка аргументов (без ключей)
    keys - ключи
    params - оригинальное сообщение без команды (с аргументами и ключами)

    """
    # new_msg_dict = {'msg': None,
    #                 'msg_without_command': None,
    #                 'msg_without_command_and_keys': None,
    #                 'command': None,
    #                 'keys': None,
    #                 'args': None,
    #                 'args_str':None
    #                 }
    msg_clear = re.sub(" +", " ", msg)
    msg_clear = re.sub(",+", ",", msg_clear)
    # Если всё поломалось, то вернуть
    # msg_clear = msg_clear.lstrip().lstrip(',').lstrip().lstrip(' ').lstrip()  # .replace(' ,', ',').replace(', ', ',')
    msg_clear = msg_clear.strip().strip(',').strip().strip(' ').strip().replace('ё', 'е')
    # .replace(' ,', ',').replace(', ', ',')

    msg_dict = {'msg': msg,
                'msg_clear': msg_clear,
                'command': None,
                'args': None,
                'original_args': None,
                'keys': None,
                'keys_list': None,
                'params': None,
                'params_without_keys': None}

    command_arg = msg_clear.split(' ', 1)
    msg_dict['command'] = command_arg[0]
    if len(command_arg) > 1:
        msg_dict['params'] = msg.replace(msg_dict['command'] + ' ', '')
        if len(msg_dict['params']) == 0:
            msg_dict['params'] = None
        msg_dict['params_without_keys'] = msg_dict['params']

        command_arg[1] = command_arg[1].replace(',', ' ')
        if command_arg[1].startswith('-'):
            command_arg[1] = " " + command_arg[1]
        find_dash = command_arg[1].find(' -')
        if find_dash != -1:
            msg_dict['keys'] = {}
            msg_dict['keys_list'] = []
        while find_dash != -1:
            next_space = command_arg[1].find(' ', find_dash + 2)
            if next_space == -1:
                next_space = len(command_arg[1])

            # for letter in command_arg[1][find_dash + 2:next_space]:
            letter = command_arg[1][find_dash + 2:next_space]
            if letter:
                msg_dict['keys'].update({letter[0]: letter[1:]})
                msg_dict['keys_list'].append(letter)

            command_arg[1] = command_arg[1][:find_dash] + command_arg[1][next_space:]
            find_dash = command_arg[1].find(' -')
        if len(command_arg[1]) > 0:
            msg_dict['args'] = command_arg[1].split(' ')
            msg_dict['original_args'] = command_arg[1].strip()

        if msg_dict['keys_list']:
            for key in msg_dict['keys_list']:
                if msg_dict['params_without_keys'][0] == '-':
                    msg_dict['params_without_keys'] = msg_dict['params_without_keys'].replace(f'-{key}', '')
                else:
                    msg_dict['params_without_keys'] = msg_dict['params_without_keys'].replace(f' -{key}', '')
    msg_dict['command'] = msg_dict['command'].lower()

    return msg_dict


def parse_attachments(vk_attachments):
    attachments = []

    if vk_attachments:
        for attachment in vk_attachments:
            attachment_type = attachment[attachment['type']]

            new_attachment = {
                'type': attachment['type']
            }
            if attachment['type'] == 'photo':
                max_size_image = attachment_type['sizes'][0]
                max_size_width = max_size_image['width']
                for size in attachment_type['sizes']:
                    if size['width'] > max_size_width:
                        max_size_image = size
                        max_size_width = size['width']
                    new_attachment['download_url'] = max_size_image['url']
                    new_attachment['size'] = {
                        'width': max_size_image['width'],
                        'height': max_size_image['height']}
            elif attachment['type'] == 'video':
                new_attachment['owner_id'] = attachment_type['owner_id']
                new_attachment['id'] = attachment_type['id']
                new_attachment['url'] = f"https://vk.com/video{attachment_type['owner_id']}_{attachment_type['id']}"
                new_attachment['title'] = attachment_type['title']
            elif attachment['type'] == 'audio':
                new_attachment['owner_id'] = attachment_type['owner_id']
                new_attachment['id'] = attachment_type['id']
                new_attachment['url'] = f"https://vk.com/audio{attachment_type['owner_id']}_{attachment_type['id']}"
                new_attachment['artist'] = attachment_type['artist']
                new_attachment['title'] = attachment_type['title']
                new_attachment['duration'] = attachment_type['duration']
                new_attachment['download_url'] = attachment_type['url']
            elif attachment['type'] == 'doc':
                new_attachment['title'] = attachment_type['title']
                new_attachment['ext'] = attachment_type['ext']
                new_attachment['download_url'] = attachment_type['url']
            elif attachment['type'] == 'wall':
                if 'attachments' in attachment_type:
                    new_attachment['attachments'] = parse_attachments(attachment_type['attachments'])
                elif 'copy_history' in attachment_type and len(attachment_type['copy_history']) > 0 and 'attachments' in \
                        attachment_type['copy_history'][0]:
                    new_attachment['attachments'] = parse_attachments(attachment_type['copy_history'][0]['attachments'])
            elif attachment['type'] == 'audio_message':
                new_attachment['id'] = attachment_type['id']
                new_attachment['owner_id'] = attachment_type['owner_id']
                new_attachment['download_url'] = attachment_type['link_mp3']
                new_attachment['duration'] = attachment_type['duration']

            attachments.append(new_attachment)

    if attachments and len(attachments) > 0:
        return attachments
    else:
        return None


def message_for_me(message, mentions):
    if message[0] == '/':
        return True
    for mention in mentions:
        if message.find(mention) != -1:
            return True
    return False


def parse_date(date):
    date_arr = date.split('.')
    if len(date_arr) == 2:
        return f"1970-{date_arr[1]}-{date_arr[0]}"
    else:
        return f"{date_arr[2]}-{date_arr[1]}-{date_arr[0]}"


def tanimoto(s1, s2):
    a, b, c = len(s1), len(s2), 0.0

    for sym in s1:
        if sym in s2:
            c += 1

    return c / (a + b - c)


class VkBotClass(threading.Thread):
    def send_message(self, peer_id, msg="ᅠ", attachments=None, keyboard=None, **kwargs):
        if attachments is None:
            attachments = []
        if type(attachments) == str:
            attachments = [attachments]
        if attachments and msg == "ᅠ":
            msg = ""
        if keyboard:
            keyboard = json.dumps(keyboard)
        msg = str(msg)
        if len(msg) > 4096:
            msg = msg[:4092]
            msg += "\n..."
        self.vk.messages.send(peer_id=peer_id,
                              message=msg,
                              access_token=self._TOKEN,
                              random_id=get_random_id(),
                              attachment=','.join(attachments),
                              keyboard=keyboard,
                              )

    def parse_and_send_msgs(self, peer_id, result):
        if type(result) == str or type(result) == int:
            result = {'msg': result}
        if type(result) == dict:
            result = [result]
        if type(result) == list:
            for msg in result:
                if type(msg) == str:
                    msg = {'msg': msg}
                if type(msg) == dict:
                    self.send_message(peer_id, **msg)

    def menu(self, vk_event, send=True):
        logger.debug(vk_event)

        if self.DEBUG and send:
            if hasattr(vk_event, 'payload') and vk_event.payload:
                debug_message = \
                    f"msg = {vk_event.msg}\n " \
                    f"command = {vk_event.command}\n " \
                    f"args = {vk_event.args}\n " \
                    f"payload = {vk_event.payload}\n "
            else:
                debug_message = \
                    f"msg = {vk_event.msg}\n " \
                    f"command = {vk_event.command}\n " \
                    f"args = {vk_event.args}\n " \
                    f"original_args = {vk_event.original_args}\n " \
                    f"keys = {vk_event.keys}\n " \
                    f"keys_list = {vk_event.keys_list}\n " \
                    f"params = {vk_event.params}\n" \
                    f"params_without_keys = {vk_event.params_without_keys}"
            self.send_message(vk_event.peer_id, debug_message)

        group = vk_event.sender.groups.filter(name='banned')
        if len(group) > 0:
            return

        # Проверяем не остановлен ли бот, если так, то проверяем вводимая команда = старт?
        if not self.check_bot_working():
            if not check_user_group(vk_event.sender, 'admin'):
                return

            if vk_event.command in ['старт']:
                self.BOT_CAN_WORK = True
                # cameraHandler.resume()
                msg = "Стартуем!"
                self.send_message(vk_event.peer_id, msg)
                logger.debug(f"{{result: {msg}}}")
                return msg
            return

        commands = get_commands()
        for command in commands:
            try:
                if command.accept(vk_event):
                    result = command.__class__().check_and_start(self, vk_event)
                    if send:
                        self.parse_and_send_msgs(vk_event.peer_id, result)
                    append_command_to_statistics(vk_event.command)
                    logger.debug(f"{{result: {result}}}")
                    return result
            except RuntimeError as e:
                msg = str(e)
                if send:
                    self.parse_and_send_msgs(vk_event.peer_id, msg)
                logger.warning(f"{{RunTimeException: {msg}}}")
                return msg
            except Exception as e:
                msg = "Ошибка. /Логи"
                if send:
                    self.parse_and_send_msgs(vk_event.peer_id, msg)
                tb = traceback.format_exc()
                print(tb)
                logs = f"Exception: {str(e)}\n" \
                       f"Traceback:\n" \
                       f"{tb}"
                logger.error(f"{{Exception: {logs}}}")
                return msg

        similar_command = commands[0].names[0]
        tanimoto_max = 0
        for command in commands:
            for name in command.names:
                tanimoto_current = tanimoto(vk_event.command, name)
                if tanimoto_current > tanimoto_max:
                    tanimoto_max = tanimoto_current
                    similar_command = name

        msg = f"Я не понял команды \"{vk_event.command}\"\n"
        if tanimoto_max >= 1:
            tanimoto_max = 1
        if tanimoto_max != 0:
            msg += f"Возможно вы имели в виду {similar_command} с вероятностью {round(tanimoto_max * 100, 2)}%"

        if send:
            self.send_message(vk_event.peer_id, msg)
        logger.debug(f"{{result: {msg}}}")
        return msg

    def __init__(self):
        super().__init__()
        self._TOKEN = secrets['vk']['TOKEN']
        self.group_id = secrets['vk']['group_id']
        vk_session = vk_api.VkApi(token=self._TOKEN, api_version="5.103")
        self.longpoll = MyVkBotLongPoll(vk_session, group_id=self.group_id)
        self.upload = VkUpload(vk_session)
        self.vk = vk_session.get_api()
        self.mentions = secrets['vk']['mentions']

        self.BOT_CAN_WORK = True
        self.DEBUG = False

    def listen_longpoll(self):
        for event in self.longpoll.listen():
            try:
                # Если пришло новое сообщение
                if event.type == VkBotEventType.MESSAGE_NEW:
                    '''
                    from_user - сообщение пришло из диалога с пользователем
                    chat_id - присутствует только в чатах
                    text - текст сообщения
                    from_id - кто отправил сообщение (если значение отрицательное, то другой бот)
                    user_id - id пользователя
                    peer_id - откуда отправил сообщение (если там значение совпадает с from_id, то это from_user, 
                        если нет и значение начинается на 200000000*, то это конфа
                    payload - скрытая информация, которая передаётся при нажатии на кнопку
                    '''

                    vk_event = {
                        'from_user': event.from_user,
                        'chat_id': event.chat_id,
                        'user_id': event.message.from_id,
                        'peer_id': event.message.peer_id,
                        'message': {
                            # 'id': event.message.id,
                            'text': event.message.text,
                            'payload': event.message.payload,
                            'attachments': event.message.attachments
                        },
                        'parsed': {
                        }}

                    if vk_event['message']['text'] is None or vk_event['message']['text'] == "":
                        continue

                    # Сообщение либо мне в лс, либо упоминание меня
                    if not (message_for_me(vk_event['message']['text'], self.mentions) or vk_event['from_user']):
                        continue

                    vk_event['message']['text'] = parse_msg_to_me(vk_event['message']['text'], self.mentions)
                    vk_event['parsed'] = parse_msg(vk_event['message']['text'])
                    vk_event['attachments'] = parse_attachments(vk_event['message']['attachments'])

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
                            self.send_message(vk_event['peer_id'],
                                              'Непредвиденная ошибка. Сообщите разработчику')
                    else:
                        vk_event['chat'] = None

                    # Обработка вложенных сообщений в vk_event['fwd']. reply и fwd для вк это разные вещи.
                    if event.message.reply_message:
                        vk_event['fwd'] = [event.message.reply_message]
                    elif len(event.message.fwd_messages) != 0:
                        vk_event['fwd'] = event.message.fwd_messages
                    else:
                        vk_event['fwd'] = None

                    vk_event_object = VkEvent(vk_event)
                    thread = threading.Thread(target=self.menu, args=(vk_event_object,))
                    thread.start()

            except Exception as e:
                print('VkBot exception\n:', e)
                print(traceback.format_exc())

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
            print('set title to', title)
        else:
            print('dont set title')

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
                vk_user.birthday = parse_date(user['bdate'])
            if 'city' in user:
                from apps.service.models import City
                city_name = user['city']['title']
                city = City.objects.filter(name=city_name)
                if len(city) > 0:
                    city = city.first()
                else:
                    city = City(name=city_name, synonyms=city_name)
                    city.save()
                vk_user.city = city
            else:
                vk_user.city = None
            if 'screen_name' in user:
                vk_user.nickname = user['screen_name']
            group_user = Group.objects.get(name='user')
            vk_user.save()
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
            raise RuntimeError("Два и более игрока подходит под поиск")
        else:
            return gamers.first()

    @staticmethod
    def get_user_by_name(args, filter_chat=None):
        if not args:
            raise RuntimeError("Отсутствуют аргументы")
        if type(args) == str:
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

        if len(user) > 1:
            raise RuntimeError("2 и более пользователей подходит под поиск")

        if len(user) == 0:
            raise RuntimeError("Пользователь не найден")

        return user.first()

    @staticmethod
    def get_chat_by_name(args):
        if not args:
            raise RuntimeError("Отсутствуют аргументы")
        if type(args) == str:
            args = [args]
        vk_chats = VkChat.objects
        for arg in args:
            vk_chats = vk_chats.filter(name__icontains=arg)

        if len(vk_chats) > 1:
            raise RuntimeError("2 и более чатов подходит под поиск")

        if len(vk_chats) == 0:
            raise RuntimeError("Чат не найден")
        return vk_chats.first()

    def get_bot_by_id(self, bot_id):
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

    def get_group_name_by_id(self, group_id):
        group = self.vk.groups.getById(group_id=group_id)[0]
        return group['name']

    @staticmethod
    def add_group_to_user(vk_user, chat):
        chats = vk_user.chats
        if chat not in chats.all():
            chats.add(chat)

    @staticmethod
    def get_group_id(id):
        return 2000000000 + int(id)

    def update_users(self):
        users = VkUser.objects.all()
        for vk_user in users:
            user = self.vk.users.get(user_id=vk_user.user_id, lang='ru', fields='sex, bdate, city, screen_name')[0]
            vk_user.name = user['first_name']
            vk_user.surname = user['last_name']
            if 'sex' in user:
                vk_user.gender = user['sex']
            if vk_user.birthday is None and 'bdate' in user:
                vk_user.birthday = parse_date(user['bdate'])
            if vk_user.city is None and 'city' in user:
                vk_user.city = user['city']['title']
            if vk_user.nickname is None and 'screen_name' in user:
                vk_user.nickname = user['screen_name']
            vk_user.save()

    def get_conversation(self):
        res = self.vk.messages.getconversation()
        print(res)

    def get_short_link(self, long_link):
        result = self.vk.utils.getShortLink(url=long_link)
        if 'short_url' in result:
            return result['short_url']
        else:
            return None

    # Проверки
    def check_bot_working(self):
        return self.BOT_CAN_WORK

    @staticmethod
    def _prepare_obj_to_upload(file_like_object, allowed_exts_url=None):
        # bytes array
        if type(file_like_object) == bytes:
            obj = io.BytesIO(file_like_object)
            obj.seek(0)
        # bytesIO
        elif type(file_like_object) == io.BytesIO:
            obj = file_like_object
            obj.seek(0)
        # url
        elif urlparse(file_like_object).hostname:
            if allowed_exts_url:
                if file_like_object.split('.')[-1].lower() not in allowed_exts_url:
                    raise RuntimeError(f"Загрузка изображений по URL доступна только для {' '.join(allowed_exts_url)}")

            response = requests.get(file_like_object, stream=True)
            obj = response.raw
        # path
        else:
            obj = file_like_object
        return obj

    def upload_photo(self, image):
        image = self._prepare_obj_to_upload(image, ['jpg', 'jpeg', 'png'])
        vk_photo = self.upload.photo_messages(image)[0]
        return self.get_attachment_by_id('photo', vk_photo['owner_id'], vk_photo['id'])

    def upload_document(self, document, peer_id, title='Документ'):
        document = self._prepare_obj_to_upload(document)
        vk_document = self.upload.document_message(document, title=title, peer_id=peer_id)['doc']
        return self.get_attachment_by_id('doc', vk_document['owner_id'], vk_document['id'])

    def get_attachment_by_id(self, type, group_id, id):
        if group_id is None:
            group_id = f'-{self.group_id}'
        return f"{type}{group_id}_{id}"


class MyVkBotLongPoll(VkBotLongPoll):
    def listen(self):
        while True:
            try:
                for event in self.check():
                    yield event
            except Exception as e:
                print('Longpoll Error (VK):', e)
