import datetime
import random
import threading

import vk_api
from vk_api import VkUpload
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id

from apps.API_VK.models import Log, VkChatId, Stream, TrustIMEI, VkUser, Winners
from apps.birds.views import snapshot
from xoma163site.settings import BASE_DIR


def user_is_admin(chat_id):
    trusted_chats = VkChatId.objects.filter(is_admin=True)
    for chat in trusted_chats:
        if chat.chat_id == str(chat_id):
            return True
    return False


def parse_msg_to_me(msg, mentions):
    for mention in mentions:
        msg = msg.replace(mention, ' ')
    return msg.lstrip().lstrip(',').lstrip().lstrip(' ').lstrip().lower()


commands_list = ['стрим', 'поток', 'где', 'синичка', 'рег', 'регистрация', 'петрович дня', 'стата', 'статистика',
                 'данет', 'рандом']
special_commands_list = ['петрович дня']


# ToDo: переписать всё это нахрен по-человечески
# ToDo: Продумать множественные аргументы
def parse_msg(msg):
    msg_dict = {'COMMAND': None, 'ARG': None}
    for item in special_commands_list:
        if msg == item:
            msg_dict['COMMAND'] = msg
            return msg_dict

    message = msg.split(' ')
    msg_dict['COMMAND'] = message[0]
    try:
        msg_dict['ARG'] = message[1]
    except Exception:
        pass
    return msg_dict


THREAD_IS_ACTIVE = False


def message_for_me(message, mentions):
    for mention in mentions:
        if message.find(mention) > -1:
            return True
    return False


class VkBot(threading.Thread):

    def send_message(self, id, msg, attachments=None):
        if attachments is None:
            attachments = []
        self.vk.messages.send(peer_id=id,
                              message=msg,
                              access_token=self._TOKEN,
                              random_id=get_random_id(),
                              attachment=','.join(attachments),
                              )

    # ToDo: Сделать у бота меню
    def menu(self, chat_id, user_id, command, arg, is_lk):
        attachments = []
        # Выбор команды
        if command == "стрим" or command == "поток":
            # Если нет аргументов
            if arg is None:
                stream = Stream.objects.first()
                self.send_message(chat_id, str(stream))
            else:
                if is_lk:
                    # Если есть права на выполнение команды
                    if user_is_admin(user_id):
                        stream = Stream.objects.first()
                        stream.link = arg
                        stream.save()
                        self.send_message(chat_id, "Ссылка изменена на " + arg)
                    else:
                        self.send_message(chat_id, "Недостаточно прав на изменение ссылки стрима")
                else:
                    self.send_message(chat_id, "Управление ботом производится только в ЛК")
        elif command == "где":
            if arg is None:
                msg = "Нет аргумента у команды 'Где'"
            else:
                user = TrustIMEI.objects.filter(name=arg.capitalize()).first()

                today = datetime.datetime.now()
                vk_event = Log.objects.filter(success=True,
                                              date__year=today.year,
                                              date__month=today.month,
                                              date__day=today.day,
                                              author=user).last()
                if user is None:
                    msg = "Такого пользователя нет"
                elif vk_event is None:
                    msg = "Информации пока ещё нет"
                else:
                    msg = "%s\n%s" % (vk_event.date.strftime("%H:%M:%S"), vk_event.msg)
            self.send_message(chat_id, str(msg))
        elif command == "синички":
            path = snapshot()
            photo = self.upload.photo_messages(path)[0]
            attachments.append('photo{}_{}'.format(photo['owner_id'], photo['id']))
            self.send_message(chat_id, "http://birds.xoma163.site", attachments=attachments)
        elif command == "рег" or command == "регистрация":
            if is_lk:
                self.send_message(chat_id, "Команда работает только в беседах.")
                return

            info = self.vk.users.get(user_id=user_id)[0]

            if VkUser.objects.filter(user_id=user_id, chat_id=chat_id).first() is not None:
                self.send_message(chat_id, "Ты уже зарегистрирован :)")
                return

            vkuser = VkUser()
            vkuser.chat_id = chat_id
            vkuser.user_id = user_id
            vkuser.username = "%s %s" % (str(info['first_name']), str(info['last_name']))
            vkuser.save()
            self.send_message(chat_id, "Регистрация прошла успешно")
        elif command == "петрович дня" or command == "петрович":
            if is_lk:
                self.send_message(chat_id, "Команда работает только в беседах.")
                return
            today = datetime.datetime.now()
            winner_today = Winners.objects.filter(date__year=today.year,
                                                  date__month=today.month,
                                                  date__day=today.day,
                                                  chat_id=chat_id).last()
            if winner_today is not None:
                self.send_message(chat_id, "Петрович дня - %s" % winner_today)
                return

            users = VkUser.objects.filter(chat_id=chat_id)
            random_int = random.randint(0, len(users) - 1)
            winner = users[random_int]

            new_winner = Winners()
            new_winner.winner = winner
            new_winner.chat_id = chat_id
            new_winner.save()
            self.send_message(chat_id, "Такс такс такс, кто тут у нас")
            self.send_message(chat_id, "Наш сегодняшний Петрович дня - %s" % winner)
        #     ToDo: Сортировать по победам
        elif command == "стата" or command == "статистика":
            players = VkUser.objects.filter(chat_id=chat_id)
            result_list = {}
            for player in players:
                result_list[player.username] = {}
                result_list[player.username]['RESULT'] = 0

            winners = Winners.objects.filter(chat_id=chat_id)
            for winner in winners:
                result_list[str(winner)]['RESULT'] += 1
            msg = "Наши любимые Петровичи:\n"

            for player in players:
                msg += "%s - %s\n" % (player.username, result_list[player.username]['RESULT'])
            self.send_message(chat_id, msg)
        elif command == "данет":
            rand_int = random.randint(0, 1)
            msg = "Да" if rand_int == 1 else "Нет"
            self.send_message(chat_id, msg)
        elif command == "рандом":
            args = arg.split(',')
            if len(args) < 2:
                self.send_message(chat_id, "Для команды рандом должно быть 2 аргумента")
                return
            try:
                int1 = int(args[0])
                int2 = int(args[1])
            except:
                self.send_message(chat_id, "Аргументы должны быть целочисленными")
                return
            if int1 > int2:
                int1, int2 = int2, int1

            rand_int = random.randint(int1, int2)
            self.send_message(chat_id, rand_int)
        #     ToDo: допилить полноценный манул
        elif command == "помощь" or command == "хелп" or command == "ман" or command == "команды":
            self.send_message(chat_id, "стрим,где N, синички, рег, петрович дня, стата, данет, рандом N,M, помощь")
        else:
            self.send_message(chat_id, "Игорь Петрович не понял команды \"%s\"" % command)

    def __init__(self):
        super().__init__()
        f = open(BASE_DIR + "/secrets/vk.txt", "r")
        self._TOKEN = f.readline().strip()
        group_id = int(f.readline().strip())
        vk_session = vk_api.VkApi(token=self._TOKEN)
        self.longpoll = MyVkBotLongPoll(vk_session, group_id=group_id)
        self.upload = VkUpload(vk_session)
        self.vk = vk_session.get_api()
        self.mentions = []
        for i in range(3):
            self.mentions.append(f.readline().strip())
        f.close()

    def listen_longpoll(self):
        for event in self.longpoll.listen():
            try:
                # Если пришло новое сообщение
                if event.type == VkBotEventType.MESSAGE_NEW:
                    message = event.object.text
                    print(message)
                    # Сообщение либо мне в лс, либо упоминание меня
                    if message_for_me(message, self.mentions) or event.object.peer_id == event.object.from_id:
                        message = parse_msg_to_me(message, self.mentions)
                        message = parse_msg(message)
                        self.menu(event.object.peer_id,
                                  event.object.from_id,
                                  message['COMMAND'],
                                  message['ARG'],
                                  event.object.peer_id == event.object.from_id)
                    else:
                        print('Сообщение не для меня :(')

            except Exception as e:
                print('ОШИБКА ВЫПОЛНЕНИЯ ЛОНГПОЛА 1:', e)

    def run(self):
        f = open('thread.lock', 'w')
        f.close()
        self.listen_longpoll()

    def get_chat_title(self, chat_id):
        return self.vk.messages.getConversationsById(peer_ids=2000000000 + chat_id)['items'][0]['chat_settings'][
            'title']

    def set_chat_title(self, chat_id, title):
        self.vk.messages.editChat(chat_id=chat_id, title=title)
        pass


class MyVkBotLongPoll(VkBotLongPoll):
    def listen(self):
        while True:
            try:
                for event in self.check():
                    yield event
            except Exception as e:
                print('ОШИБКА ВЫПОЛНЕНИЯ ЛОНГПОЛА 2:', e)
