# ToDo: Yandex translate
# https://translate.yandex.net/api/v1.5/tr.json/translate?lang=ru-en &key=trnsl.1.1.20190926T183128Z.8452015e2670796c.b68628c3dc7cd243cfacdbc62da980a41435cb43&text=Привет, как дела?
# Разобраться с ответками.


import datetime
import json
import random
import re
import threading

import vk_api
from django.core.paginator import Paginator
from vk_api import VkUpload
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id

from apps.API_VK.models import Log, Stream, VkUser, QuoteBook, PetrovichUser, PetrovichGames
from apps.API_VK.static_texts import get_help_text, get_insults, get_praises, get_bad_words, get_bad_answers, \
    get_sorry_phrases, get_keyboard
from xoma163site.settings import BASE_DIR
from xoma163site.wsgi import cameraHandler


def parse_msg_to_me(msg, mentions):
    for mention in mentions:
        msg = msg.replace(mention, '')
    msg = re.sub(" +", " ", msg)
    return msg.lstrip().lstrip(',').lstrip().lstrip(' ').lstrip().replace(' ,', ',').replace(', ', ',')


def parse_msg(msg):
    msg_dict = {'command': None, 'args': None}

    command_arg = msg.split(' ', 1)
    msg_dict['command'] = command_arg[0].lower()
    if len(command_arg) > 1:
        command_arg[1] = command_arg[1].replace(' ', ',')
        msg_dict['args'] = command_arg[1].split(',')
    else:
        msg_dict['args'] = None

    return msg_dict


THREAD_IS_ACTIVE = False


def message_for_me(message, mentions):
    if message[0] == '/':
        return True
    for mention in mentions:
        if message.find(mention) > -1:
            return True
    return False


def get_random_item_from_list(list, arg=None):
    rand_int = random.randint(0, len(list) - 1)
    if arg:
        msg = "{}, ты {}".format(arg, list[rand_int].lower())
    else:
        msg = list[rand_int]
    return msg


class VkBot(threading.Thread):

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
        user_id = vk_event['message']['user_id']
        peer_id = vk_event['message']['peer_id']

        command = vk_event['message']['text']['command']
        args = vk_event['message']['text']['args']
        is_lk = vk_event['from_user']
        full_message = vk_event['message']['full_text']

        if is_lk:
            chat_id = user_id
        else:
            chat_id = peer_id

        # DEBUG
        # self.send_message(chat_id, "Команда:{}\n "
        #                            "Аргументы:{}\n".format(str(command), str(args)))

        sender = self.get_user_by_id(user_id, chat_id)

        if sender.is_banned:
            self.send_message(chat_id, "У тебя бан")
            return
        # Проверяем не остановлен ли бот, если так, то проверяем вводимая команда = старт?
        if not self.BOT_CAN_WORK:
            if sender.is_admin:
                if command in ['старт']:
                    self.BOT_CAN_WORK = True
                    cameraHandler.resume()
                    self.send_message(chat_id, "Стартуем!")
                    return
                else:
                    return
            else:
                self.send_message(chat_id, "Недостаточно прав на возобновление бота")
            return

        attachments = []
        # Выбор команды
        if command in ["стрим", "поток"]:
            # Если нет аргументов
            if args is None:
                stream = Stream.objects.first()
                if len(str(stream)) < 5:
                    self.send_message(chat_id, "Стрим пока не идёт")
                    return
                else:
                    self.send_message(chat_id, str(stream))
                    return
            else:
                if not is_lk:
                    self.send_message(chat_id, "Управление ботом производится только в ЛК")
                    return
                    # Если есть права на выполнение команды

                if not sender.is_admin:
                    self.send_message(chat_id, "Недостаточно прав на изменение ссылки стрима")
                    return
                stream = Stream.objects.first()
                stream.link = args[0]
                stream.save()
                self.send_message(chat_id, "Ссылка изменена на " + args[0])
                return
        elif full_message[-1] == '?':
            bad_words = get_bad_words()

            min_index_bad = len(full_message)
            max_index_bad = -1
            for word in bad_words:
                ind = full_message.lower().find(word)
                if ind != -1:
                    if ind < min_index_bad:
                        min_index_bad = ind
                    if ind > max_index_bad:
                        max_index_bad = ind

            min_index_bad = full_message.rfind(' ', 0, min_index_bad)
            if min_index_bad == -1:
                min_index_bad = full_message.rfind(',', 0, min_index_bad)
                if min_index_bad == -1:
                    min_index_bad = full_message.rfind('.', 0, min_index_bad)
                    if min_index_bad == -1:
                        min_index_bad = full_message.find('/')
            min_index_bad += 1

            if max_index_bad != -1:
                len_bad = full_message.find(',', max_index_bad)
                if len_bad == -1:
                    len_bad = full_message.find(' ', max_index_bad)
                    if len_bad == -1:
                        len_bad = full_message.find('?', max_index_bad)

                bad_answers = get_bad_answers()
                rand_int = random.randint(0, len(bad_answers) - 1)
                self.send_message(chat_id, bad_answers[rand_int])
                name = sender.name
                if sender.gender == 1:
                    msg_self = "сама"
                else:
                    msg_self = "сам"
                msg = "{}, {} {} {}?".format(name, "может ты", msg_self, full_message[min_index_bad: len_bad])
                self.send_message(chat_id, msg)
                return

            rand_int = random.randint(1, 100)
            if rand_int <= 48:
                msg = "Да"
            elif rand_int <= 96:
                msg = "Нет"
            else:
                msg = "Ну тут даже я хз"
            self.send_message(chat_id, msg)
            return
        elif command in ["где"]:
            if args is None:
                self.send_message(chat_id, "Нет аргумента у команды 'Где'")
                return
            elif len(args) > 1:
                user = VkUser.objects.filter(name=args[0].capitalize(), surname=args[1].capitalize(),
                                             chat_id=chat_id).first()
            else:
                user = VkUser.objects.filter(name=args[0].capitalize()).first()

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
            return
        elif command in ["c", "с", "синички"]:
            try:
                # path = snapshot()
                path = cameraHandler.get_img()
            except RuntimeError as e:
                print(e)
                return
            frames = 20
            quality = 0

            try:
                if args:
                    try:
                        frames = int(args[0])
                        if frames > cameraHandler.MAX_FRAMES:
                            self.send_message(chat_id,
                                              "Ты совсем поехавший? До {} кадров давай".format(
                                                  cameraHandler.MAX_FRAMES))
                            return
                    except:
                        self.send_message(chat_id, "Введите количество кадров в gif")
                        return
                    if len(args) > 1:
                        try:
                            quality = int(args[1])
                            if not 0 <= quality <= 1:
                                self.send_message(chat_id, "Качество может быть в диапазоне [0,1]")
                                return
                        except:
                            self.send_message(chat_id, "Качество может быть в диапазоне [0,1]")
                            return
            except:
                pass

            photo = self.upload.photo_messages(path)[0]
            attachments.append('photo{}_{}'.format(photo['owner_id'], photo['id']))

            if frames != 0:
                try:
                    path2 = cameraHandler.get_gif(frames, quality == 1)
                except RuntimeError as e:
                    self.send_message(chat_id, e)
                    return
                gifka = self.upload.document_message(path2, title='Синички', peer_id=chat_id)['doc']
                attachments.append('doc{}_{}'.format(gifka['owner_id'], gifka['id']))

            self.send_message(chat_id, "http://birds.xoma163.xyz", attachments=attachments)
            return
        elif command in ["рег", "регистрация"]:
            if is_lk:
                self.send_message(chat_id, "Команда работает только в беседах.")
                return

            if sender.is_admin:
                if args:
                    user_id = int(args[0])

            vk_user = VkUser.objects.filter(user_id=user_id).first()
            if vk_user is not None:
                if PetrovichUser.objects.filter(user=vk_user, chat_id=chat_id).first() is not None:
                    self.send_message(chat_id, "Ты уже зарегистрирован :)")
                    return

            p_user = PetrovichUser()
            p_user.user = sender
            p_user.chat_id = chat_id
            p_user.save()

            self.send_message(chat_id, "Регистрация прошла успешно")
            return
        elif command in ["петрович", "петр"]:
            if is_lk:
                self.send_message(chat_id, "Команда работает только в беседах.")
                return
            today = datetime.datetime.now()
            winner_today = PetrovichGames.objects.filter(date__year=today.year,
                                                         date__month=today.month,
                                                         date__day=today.day,
                                                         chat_id=chat_id).last()
            if winner_today is not None:
                self.send_message(chat_id, "Петрович дня - %s" % winner_today.user)
                return

            users = PetrovichUser.objects.filter(chat_id=chat_id)
            random_int = random.randint(0, len(users) - 1)
            winner = users[random_int].user
            PetrovichGames.objects.filter(chat_id=chat_id).delete()
            new_winner = PetrovichGames()
            new_winner.user = winner
            new_winner.chat_id = chat_id
            new_winner.save()
            self.send_message(chat_id, "Такс такс такс, кто тут у нас")
            self.send_message(chat_id, "Наш сегодняшний Петрович дня - %s" % winner)
            return
        elif command in ["стата", "статистика"]:
            players = PetrovichUser.objects.filter(chat_id=chat_id)
            result_list = []
            for player in players:
                result_list.append([player, player.wins])

            msg = "Наши любимые Петровичи:\n"
            result_list.sort(key=lambda i: i[1], reverse=True)

            for result in result_list:
                msg += "%s - %s\n" % (result[0], result[1])
            self.send_message(chat_id, msg)
            return
        elif command in ["рандом", "ранд"]:
            if len(args) == 2:
                try:
                    int1 = int(args[0])
                    int2 = int(args[1])
                except:
                    self.send_message(chat_id, "Аргументы должны быть целочисленными")
                    return
            else:
                int1 = 1
                try:
                    int2 = int(args[0])
                except:
                    self.send_message(chat_id, "Аргументы должны быть целочисленными")
                    return

            if int1 > int2:
                int1, int2 = int2, int1

            rand_int = random.randint(int1, int2)
            self.send_message(chat_id, rand_int)
            return
        elif command in ["спасибо", "спасибо!", "спс"]:
            self.send_message(chat_id, "Всегда пожалуйста! :)")
            return
        elif command in ['сори', 'прости', 'извини']:
            phrases = get_sorry_phrases()
            msg = get_random_item_from_list(phrases)
            self.send_message(chat_id, msg)
            return
        elif command in ["помощь", "хелп", "ман", "команды", "помоги", "памаги", "спаси", "хелб"]:
            self.send_message(chat_id, get_help_text(sender.is_admin, sender.is_student))
            return
        elif command in ["погода"]:
            if args is None:
                city = 'самара'
            else:
                city = args[0].lower()
            from apps.API_VK.yandex_weather import get_weather

            weather = get_weather(city)

            self.send_message(chat_id, weather)
            return
        elif command in ["похвалить", "похвали", "хвалить"]:
            if args:
                if args[0].lower() == "петрович":
                    msg = "спс))"
                else:
                    msg = get_random_item_from_list(get_praises(), args[0])
            else:
                msg = get_random_item_from_list(get_praises())
            self.send_message(chat_id, msg)
            return
        elif command in ["обосрать", "обосри"]:
            if args:
                if args[0].lower() == "петрович":
                    msg = get_random_item_from_list(get_bad_answers())
                else:
                    msg = get_random_item_from_list(get_insults(), args[0])
            else:
                msg = get_random_item_from_list(get_insults())
            self.send_message(chat_id, msg)
            return
        elif command in ["цитата", "(c)", "(с)"]:
            if not 'fwd' in vk_event:
                self.send_message(chat_id, "Перешлите сообщения для сохранения цитаты")
                return
            msgs = vk_event['fwd']

            quote = QuoteBook()
            quote.peer_id = peer_id
            quote.user_id = 0
            if len(msgs) == 1:
                if msgs[0]['from_id'] > 0:
                    quote.username = sender.name + " " + sender.surname
                else:
                    quote.username = self.get_groupname_by_id(int(msgs[0]['from_id']) * -1)
            else:
                quote.username = ""
            quote_text = ""
            for msg in msgs:
                text = msg['text']
                if msg['from_id'] > 0:
                    username = sender.name + " " + sender.surname
                else:
                    username = self.get_groupname_by_id(int(msg['from_id']) * -1)
                quote_text += "{}\n{}\n\n".format(username, text)
            quote.text = quote_text
            quote.save()
            self.send_message(chat_id, "Цитата сохранена")
            return
        elif command in ["цитаты"]:
            text_filter = None
            if args is not None:
                if len(args) == 2:
                    try:
                        page = int(args[1])
                    except:
                        self.send_message(chat_id, "Номер страницы должен быть целочисленным")
                        return
                    if page <= 0:
                        self.send_message(chat_id, "Номер страницы должен быть положительным")
                        return
                    text_filter = args[0]
                elif len(args) == 1:
                    try:
                        page = int(args[0])
                        if page <= 0:
                            self.send_message(chat_id, "Номер страницы должен быть положительным")
                            return
                    except:
                        page = 1
                        text_filter = args[0]
                else:
                    self.send_message(chat_id, "Неверное количество аргументов")
                    return

                if text_filter is not None:
                    objs = QuoteBook.objects.filter(text__icontains=text_filter)
                else:
                    objs = QuoteBook.objects.all()
            else:
                objs = QuoteBook.objects.all()
                page = 1
            objs = objs.filter(peer_id=peer_id).order_by('-date')
            p = Paginator(objs, 5)

            if page > p.num_pages:
                self.send_message(chat_id, "Такой страницы нет. Последняя страница - {}".format(p.num_pages))
                return

            objs_on_page = p.page(page)
            msg = "Страница {}/{}\n\n".format(page, p.num_pages)
            for i, obj_on_page in enumerate(objs_on_page):
                msg += "------------------------------{}------------------------------\n" \
                       "{}\n" \
                       "(c) {} {}\n".format(i + 1, obj_on_page.text,
                                            obj_on_page.username,
                                            obj_on_page.date.strftime(
                                                "%d.%m.%Y %H:%M:%S"))

            self.send_message(chat_id, msg)
            return
        elif command in ["клава", "клавиатура"]:
            print(sender.is_admin)
            print(sender.is_student)
            self.send_message(chat_id, 'Лови',
                              keyboard=json.dumps(get_keyboard(sender.is_admin, sender.is_student)))
            return
        elif command in ["убери", "скрыть"]:
            keyboard = {
                "one_time": False,
                "buttons": []
            }
            self.send_message(chat_id, 'Убрал', keyboard=json.dumps(keyboard))
            return
        elif command in ["уъу", "бля", "ъуъ"]:

            if not 'fwd' in vk_event:
                self.send_message(chat_id, "Перешлите сообщения для уъуфикации")
                return

            msgs = vk_event['fwd']

            if len(msgs) == 1:
                new_msg = msgs[0]['text']
            else:
                new_msg = ""
                for msg in msgs:
                    new_msg += msg['text'] + "\n"
            symbols = ['.', ',', '?', '!', ':', '—', '-']
            flag = False
            if new_msg[-1] not in symbols:
                new_msg += '.'
                flag = True
            for symbol in symbols:
                new_msg = new_msg.replace(symbol, " бля" + symbol)
            if flag:
                new_msg = new_msg[:-1]
            # new_msg = new_msg.replace('блябля', 'бля').replace('бля бля', 'бля')
            self.send_message(chat_id, new_msg)
            return
        elif command in ["привет", "хай", "даров", "дарова", "здравствуй", "здравствуйте", "привки", "прив", "q", "qq",
                         "ку", "куку", "здаров", "здарова"]:
            self.send_message(chat_id, 'Хай')
            return
        elif command in ["пока", "бай", "bb", "бай-бай", "байбай", "бб", "досвидос", "до встречи", "бывай"]:
            self.send_message(chat_id, 'Пока((')
            return
        elif command in ["дерьмо"]:
            self.send_message(chat_id, "ня")
            return
        elif command in ["ня"]:
            self.send_message(chat_id, "дерьмо")
            return
        elif command in ["гит"]:
            self.send_message(chat_id, "https://github.com/Xoma163/xoma163site/")
            return
        elif command in ["донат"]:
            self.send_message(chat_id, "https://www.donationalerts.com/r/xoma163")
            return
        #     -----------------------------------------
        elif command in ["расписание", "расп"]:
            photo = {'owner_id': -186416119, 'id': 457239626}
            attachments.append('photo{}_{}'.format(photo['owner_id'], photo['id']))
            self.send_message(chat_id, str((datetime.datetime.now().isocalendar()[1] - 35)) + " неделя",
                              attachments=attachments)
            return
        elif command in ["гугл", "ссылка", "учебное"]:
            self.send_message(chat_id, "https://drive.google.com/open?id=1AJPnT2XXYNc39-2CSr_MzHnv4hs6Use6")
            return
        elif command in ["лекции"]:
            self.send_message(chat_id, "https://drive.google.com/open?id=19QVRRbj6ePEFTxS2bHOjjaKljkJwZxNB")
            return
        elif command in ["неделя"]:
            self.send_message(chat_id, str((datetime.datetime.now().isocalendar()[1] - 35)) + " неделя")
            return
        #     -----------------------------------------
        elif command in ["управление", "сообщение"]:
            if not is_lk:
                self.send_message(chat_id, "Управление ботом производится только в ЛК")
                return
            if args is None:
                self.send_message(chat_id, "Отсутствуют аргументы chat_id и сообщение")
                return
            msg_chat_id = int(args[0])
            msg = args[1]
            if not sender.is_admin:
                self.send_message(chat_id, "Недостаточно прав на изменение ссылки стрима")
                return

            self.send_message(2000000000 + msg_chat_id, msg)
            return
        elif command in ["стоп"]:
            if not sender.is_admin:
                text = "бота"
                if args[0] == "синички":
                    text = "синичек"
                self.send_message(chat_id, "Недостаточно прав на остановку {}".format(text))
                return
            if args[0] == "синички":
                if cameraHandler._running:
                    cameraHandler.terminate()
                    self.send_message(chat_id, "Финишируем синичек")
                else:
                    self.send_message(chat_id, "Синички уже финишировали")
                return
            self.BOT_CAN_WORK = False
            self.send_message(chat_id, "Финишируем")
            return
        elif command in ["старт"]:
            if not sender.is_admin:
                self.send_message(chat_id, "Недостаточно прав на старт синичек")
                return
            if args[0] == "синички":
                if not cameraHandler._running:
                    cameraHandler.resume()
                    self.send_message(chat_id, "Стартуем синичек!")
                else:
                    self.send_message(chat_id, "Синички уже стартовали!")
                return
        elif command in ["команда"]:
            if not sender.is_admin:
                self.send_message(chat_id, "Недостаточно прав на выполнение команд")
                return
            if args[0] is None:
                self.send_message(chat_id, "Нет параметров у команды")
                return

            # process = subprocess.Popen(arg.split(), stdout=subprocess.PIPE)
            # output, error = process.communicate()
            # output = output.decode("utf-8")
            # if error:
            #     output += "\n{}".format(error)
            # self.send_message(chat_id, output)
        elif command in ["бан"]:
            if not sender.is_admin:
                self.send_message(chat_id, "Недостаточно прав на бан")
                return

            if args is None:
                self.send_message(chat_id, "Нет аргумента у команды 'бан'")
                return
            elif len(args) > 1:
                user = VkUser.objects.filter(name=args[0].capitalize(), surname=args[1].capitalize()).first()
            else:
                user = VkUser.objects.filter(name=args[0].capitalize()).first()

            if user is None:
                self.send_message(chat_id, "Пользователь не найден")
                return

            if user.is_admin:
                self.send_message(chat_id, "Нельзя банить админа")
                return
            user.is_banned = True
            user.save()

            self.send_message(chat_id, "Забанен")
            return
        elif command in ["разбан"]:
            if not sender.is_admin:
                self.send_message(chat_id, "Недостаточно прав на разбан")
                return

            if args is None:
                self.send_message(chat_id, "Нет аргумента у команды 'разбан'")
                return
            elif len(args) > 1:
                user = VkUser.objects.filter(name=args[0].capitalize(), surname=args[1].capitalize()).first()
            else:
                user = VkUser.objects.filter(name=args[0].capitalize()).first()
            if user is None:
                self.send_message(chat_id, "Пользователь не найден")
                return
            user.is_banned = False
            user.save()
            self.send_message(chat_id, "Разбанен")
            return
        # elif command in ["рестарт"]:
        #     if not sender.is_admin:
        #         self.send_message(chat_id, "Недостаточно прав на рестарт")
        #         return
        #     self.send_message(chat_id, "Разбанен")

        else:
            self.send_message(chat_id, "Я не понял команды \"%s\"" % command)
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

                    # Сообщение либо мне в лс, либо упоминание меня
                    if message_for_me(vk_event['message']['text'], self.mentions) or vk_event['from_user']:

                        # Обрезаем палку
                        if vk_event['message']['text'][0] == '/':
                            vk_event['message']['text'] = vk_event['message']['text'][1:]

                        vk_event['message']['text'] = parse_msg_to_me(vk_event['message']['text'], self.mentions)
                        vk_event['message']['text'] = parse_msg(vk_event['message']['text'])

                        thread = threading.Thread(target=self.menu, args=(vk_event,))
                        thread.start()
                        # self.menu(vk_event)

                    else:
                        print('Сообщение не для меня :(')

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
        pass

    def set_chat_title_if_not_equals(self, chat_id, title):
        if title != self.vk.messages.getConversationsById(peer_ids=2000000000 + chat_id)['items'][0]['chat_settings'][
            'title']:
            self.vk.messages.editChat(chat_id=chat_id, title=title)
            print('set title to', title)
        else:
            print('dont set title')

    def get_user_by_id(self, user_id, chat_id):
        vk_user = VkUser.objects.filter(user_id=user_id)
        if len(vk_user) > 0:
            vk_user = vk_user.first()
            # user = {'name': vk_user.name, 'surname': vk_user.surname, 'gender': vk_user.gender}
        else:
            # Прозрачная регистрация
            user = self.vk.users.get(user_id=user_id, lang='ru', fields='sex')[0]
            vk_user = VkUser()
            vk_user.user_id = user_id
            vk_user.name = user['first_name']
            vk_user.surname = user['last_name']
            vk_user.gender = user['sex']

            if chat_id == 2000000003:
                vk_user.is_student = True
            vk_user.save()

        return vk_user

    def get_groupname_by_id(self, group_id):
        group = self.vk.groups.getById(group_id=group_id)[0]
        return group['name']

    # def register_user(self, user_id, chat_id):
    #     vk_user = VkUser()
    #     vk_user.user_id = user_id
    #     user = self.get_user_by_id(user_id)
    #     vk_user.name = user['name']
    #     vk_user.surname = user['surname']
    #     vk_user.gender = user['gender']
    #
    #     if chat_id == 2000000003:
    #         vk_user.is_student = True
    #     vk_user.save()
    #     return vk_user


class MyVkBotLongPoll(VkBotLongPoll):
    def listen(self):
        while True:
            try:
                for event in self.check():
                    yield event
            except Exception as e:
                print('ОШИБКА ВЫПОЛНЕНИЯ ЛОНГПОЛА 2:', e)
