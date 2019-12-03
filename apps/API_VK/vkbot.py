import re
import threading

import vk_api
from vk_api import VkUpload
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id

from apps.API_VK.command import get_commands
from apps.API_VK.models import VkUser, VkBot, VkChat
from apps.Statistics.views import append_command_to_statistics
from xoma163site.settings import BASE_DIR
from xoma163site.wsgi import cameraHandler


def parse_msg_to_me(msg, mentions):
    for mention in mentions:
        msg = msg.replace(mention, '')
    msg = re.sub(" +", " ", msg)
    return msg.lstrip().lstrip(',').lstrip().lstrip(' ').lstrip().replace(' ,', ',').replace(', ', ',')


def parse_msg(msg):
    msg_dict = {'command': None, 'args': None, 'original_args': None}

    command_arg = msg.split(' ', 1)
    msg_dict['command'] = command_arg[0].lower()
    if len(command_arg) > 1:
        command_arg[1] = command_arg[1].replace(',', ' ')
        msg_dict['original_args'] = command_arg[1]
        msg_dict['args'] = command_arg[1].split(' ')
    else:
        msg_dict['args'] = None

    return msg_dict


def message_for_me(message, mentions):
    if message[0] == '/':
        return True
    for mention in mentions:
        if message.find(mention) > -1:
            return True
    return False


def parse_date(date):
    date_arr = date.split('.')
    if len(date_arr) == 2:
        return "{}-{}-{}".format(1970, date_arr[1], date_arr[0])
    else:
        return "{}-{}-{}".format(date_arr[2], date_arr[1], date_arr[0])


class VkBotClass(threading.Thread):

    def send_message(self, peer_id, msg, attachments=None, keyboard=None):
        if attachments is None:
            attachments = []

        if len(msg) > 4096:
            msg = msg[:4092]
            msg += "\n..."
        self.vk.messages.send(peer_id=peer_id,
                              message=msg,
                              access_token=self._TOKEN,
                              random_id=get_random_id(),
                              attachment=','.join(attachments),
                              keyboard=keyboard
                              )

    def menu(self, vk_event):
        if vk_event.sender.is_banned:
            self.send_message(vk_event.chat_id, "У вас бан")
            return
        # Проверяем не остановлен ли бот, если так, то проверяем вводимая команда = старт?
        if not self.check_bot_working():
            if not vk_event.sender.is_admin:
                return

            if vk_event.command in ['старт']:
                self.BOT_CAN_WORK = True
                cameraHandler.resume()
                self.send_message(vk_event.chat_id, "Стартуем!")
                return
            return

        commands = get_commands()
        for command in commands:
            try:
                if command.accept(self, vk_event):
                    append_command_to_statistics(vk_event.command)
                    return
            except RuntimeError as e:
                return
        self.send_message(vk_event.chat_id, "Я не понял команды \"%s\"" % vk_event.command)
        return

    def __init__(self):
        super().__init__()
        f = open(BASE_DIR + "/secrets/vk.txt")
        self._TOKEN = f.readline().strip()
        self._group_id = int(f.readline().strip())
        vk_session = vk_api.VkApi(token=self._TOKEN)
        self.longpoll = MyVkBotLongPoll(vk_session, group_id=self._group_id)
        self.upload = VkUpload(vk_session)
        self.vk = vk_session.get_api()
        self.mentions = []
        self.BOT_CAN_WORK = True
        for i in range(3):
            self.mentions.append(f.readline().strip())
        f.close()

    def listen_longpoll(self):
        for event in self.longpoll.listen():
            try:
                # Если пришло новое сообщение
                if event.type == VkBotEventType.MESSAGE_NEW:
                    vk_event = {'from_chat': event.from_chat,
                                'from_group': event.from_group,
                                'from_user': event.from_user,
                                'chat_id': event.chat_id,
                                'message': {
                                    'text': event.object.text,
                                    'full_text': event.object.text,
                                    'user_id': event.object.from_id,
                                    'peer_id': event.object.peer_id,
                                }}

                    if 'reply_message' in event.object:
                        vk_event['fwd'] = [event.object['reply_message']]
                    elif 'fwd_messages' in event.object:
                        if len(event.object['fwd_messages']) != 0:
                            vk_event['fwd'] = event.object['fwd_messages']
                        else:
                            vk_event['fwd'] = None

                    # Сообщение либо мне в лс, либо упоминание меня
                    if message_for_me(vk_event['message']['text'], self.mentions) or vk_event['from_user']:

                        # Обрезаем палку
                        if vk_event['message']['text'][0] == '/':
                            vk_event['message']['text'] = vk_event['message']['text'][1:]

                        vk_event['message']['text'] = parse_msg_to_me(vk_event['message']['text'], self.mentions)
                        vk_event['message']['text'] = parse_msg(vk_event['message']['text'])

                        if vk_event['message']['user_id'] > 0:
                            vk_event['sender'] = self.get_user_by_id(vk_event['message']['user_id'])
                        else:
                            self.send_message(vk_event['message']['peer_id'], "Боты не могут общаться с Петровичем")
                            continue
                        if vk_event['chat_id']:
                            vk_event['chat'] = self.get_chat_by_id(int(vk_event['chat_id']))
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
                print('ОШИБКА ВЫПОЛНЕНИЯ ЛОНГПОЛА 1:', e)

    def run(self):
        open('thread.lock', 'w')
        self.listen_longpoll()

    def get_chat_title(self, chat_id):
        return self.vk.messages.getConversationsById(peer_ids=2000000000 + chat_id)['items'][0]['chat_settings'][
            'title']

    def set_chat_title(self, chat_id, title):
        self.vk.messages.editChat(chat_id=chat_id, title=title)

    def set_chat_title_if_not_equals(self, chat_id, title):
        if title != self.vk.messages.getConversationsById(peer_ids=2000000000 + chat_id)['items'][0]['chat_settings'][
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
                vk_user.birthday = user['bdate']
            if 'city' in user:
                vk_user.birthday = parse_date(user['bdate'])
            if 'screen_name' in user:
                vk_user.nickname = user['screen_name']
            vk_user.save()
        return vk_user

    @staticmethod
    def get_user_by_name(args):
        if not args:
            raise RuntimeError("Отсутствуют аргументы")
        if len(args) >= 2:
            user = VkUser.objects.filter(name=args[0].capitalize(), surname=args[1].capitalize())
        else:
            user = VkUser.objects.filter(name=args[0].capitalize())
            if len(user) == 0:
                user = VkUser.objects.filter(surname=args[0].capitalize())
                if len(user) == 0:
                    user = VkUser.objects.filter(nickname=args[0])
        if len(user) > 1:
            raise RuntimeError("2 и более пользователей подходит под поиск")

        if len(user) == 0:
            raise RuntimeError("Пользователь не найден")

        return user.first()

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
            # Прозрачная регистрация
            vk_chat = VkChat()
            vk_chat.chat_id = chat_id
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
        return 2000000000 + id

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

    def get_conversations(self):
        res = self.vk.messages.getConversations()
        print(res)

    # Проверки

    def check_bot_working(self):
        return self.BOT_CAN_WORK


class MyVkBotLongPoll(VkBotLongPoll):
    def listen(self):
        while True:
            try:
                for event in self.check():
                    yield event
            except Exception as e:
                print('ОШИБКА ВЫПОЛНЕНИЯ ЛОНГПОЛА 2:', e)


class VkEvent:
    def __init__(self, vk_event):
        self.user_id = vk_event['message']['user_id']
        self.peer_id = vk_event['message']['peer_id']

        self.command = vk_event['message']['text']['command']
        self.args = vk_event['message']['text']['args']
        self.original_args = vk_event['message']['text']['original_args']
        self.is_lk = vk_event['from_user']
        self.full_message = vk_event['message']['full_text']
        self.fwd = vk_event['fwd']

        if self.is_lk:
            self.chat_id = self.user_id
        else:
            self.chat_id = self.peer_id

        self.sender = vk_event['sender']
        if vk_event['chat']:
            self.chat = vk_event['chat']
