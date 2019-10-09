# ToDo: Yandex translate
# https://translate.yandex.net/api/v1.5/tr.json/translate?lang=ru-en &key=trnsl.1.1.20190926T183128Z.8452015e2670796c.b68628c3dc7cd243cfacdbc62da980a41435cb43&text=Привет, как дела?
# Разобраться с ответками.


import datetime
import random
import threading

import vk_api
from vk_api import VkUpload
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id

from apps.API_VK.models import Log, VkChatId, Stream, TrustIMEI, VkUser, Winners
from apps.birds.views import snapshot, gif
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

special_commands_list = ['петрович дня']

# ToDo: переписать всё это нахрен по-человечески
def parse_msg(msg):
    msg_dict = {'COMMAND': None, 'ARG': None}

    for item in special_commands_list:
        if msg == item:
            msg_dict['COMMAND'] = msg
            return msg_dict

    message = [None, None]
    # Парс команды с пробелами
    first_space = msg.find(' ')
    # Добавил в условие =, хз чё сломает
    first_space = first_space if first_space >= 1 else len(msg)
    message[0] = msg[0:first_space]
    message[1] = msg[first_space + 1:len(msg)]

    if message[1] in ['', ' ']:
        message[1] = None

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

    def menu(self, chat_id, user_id, command, arg, is_lk, full_message):
        print('chat_id', chat_id, 'user_id', user_id, 'command', command, 'arg', arg, 'is_lk', is_lk, 'full_message',
              full_message)
        attachments = []
        # Выбор команды
        if command in ["стрим", "поток"]:
            # Если нет аргументов
            if arg is None:
                stream = Stream.objects.first()
                if len(str(stream)) < 5:
                    self.send_message(chat_id, "Стрим пока не идёт")
                else:
                    self.send_message(chat_id, str(stream))
            else:
                if not is_lk:
                    self.send_message(chat_id, "Управление ботом производится только в ЛК")
                    return
                    # Если есть права на выполнение команды

                if not user_is_admin(user_id):
                    self.send_message(chat_id, "Недостаточно прав на изменение ссылки стрима")
                    return
                stream = Stream.objects.first()
                stream.link = arg
                stream.save()
                self.send_message(chat_id, "Ссылка изменена на " + arg)
        elif command in ["где"]:
            if arg is None:
                msg = "Нет аргумента у команды 'Где'"
                return
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
        elif command in ["c", "с", "синички", "кормушка"]:

            # if user_id == 68902868 or user_id == 23269243:
            #     self.send_message(chat_id, "Временный бан")
            #     return

            path = snapshot()
            frames = 20
            if arg:
                try:
                    frames = int(arg)
                    # ToDo: ограниченное число запросов
                    if frames > 100:
                        self.send_message(chat_id, "Ты совсем поехавший? До 100 кадров давай")
                        return
                except:
                    self.send_message(chat_id, "Введите количество кадров в gif")
                    return
            photo = self.upload.photo_messages(path)[0]
            attachments.append('photo{}_{}'.format(photo['owner_id'], photo['id']))

            if frames != 0:
                path2 = gif(frames)
                gifka = self.upload.document_message(path2, title='Синички', peer_id=chat_id)['doc']
                attachments.append('doc{}_{}'.format(gifka['owner_id'], gifka['id']))

            self.send_message(chat_id, "http://birds.xoma163.site", attachments=attachments)
        elif command in ["рег", "регистрация"]:
            if is_lk:
                self.send_message(chat_id, "Команда работает только в беседах.")
                return

            info = self.vk.users.get(user_id=user_id, lang='ru')[0]

            if VkUser.objects.filter(user_id=user_id, chat_id=chat_id).first() is not None:
                self.send_message(chat_id, "Ты уже зарегистрирован :)")
                return

            vkuser = VkUser()
            vkuser.chat_id = chat_id
            vkuser.user_id = user_id
            vkuser.username = "%s %s" % (str(info['first_name']), str(info['last_name']))
            vkuser.save()
            self.send_message(chat_id, "Регистрация прошла успешно")
        elif command in ["петрович дня", "петрович"]:
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
        elif command in ["стата", "статистика"]:
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
        elif command in ["данет"] or full_message[-1] == '?':
            bad_words = ['еба', 'ёба', 'пидор', 'пидар', "пидр", 'гандон', 'годнон', 'хуй', 'пизд', 'бля', 'шлюха',
                         'мудак', 'говно', 'моча', 'залупа', 'гей', 'сука', 'дурак', 'говно', 'жопа', 'ублюдок',
                         'мудак']

            min_index_bad = len(full_message)
            max_index_bad = -1
            print('min_index_bad', min_index_bad)
            print('max_index_bad', max_index_bad)
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

                print('len_bad', len_bad)
                bad_answers = ['как же вы меня затрахали...', 'ты обижаешь бота?', 'тебе заняться нечем?', '...',
                               'о боже']
                rand_int = random.randint(0, len(bad_answers) - 1)
                self.send_message(chat_id, bad_answers[rand_int])
                user = self.vk.users.get(user_id=user_id, lang='ru', fields='sex')[0]
                first_name = user['first_name']
                if user['sex'] == 1:
                    msg_self = "сама"
                else:
                    msg_self = "сам"
                print(user['sex'])
                msg = "{}, {} {} {}?".format(first_name, "может ты", msg_self, full_message[min_index_bad: len_bad])
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
        elif command in ["рандом", "ранд"]:
            args = arg.split(',')
            # ToDo: читать в любом случае
            # except если оба хрень
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
        elif command in ["спасибо", "спасибо!", "спс"]:
            self.send_message(chat_id, "Всегда пожалуйста! :)")
        elif command in ["помощь", "хелп", "ман", "команды", "помоги", "памаги"]:
            self.send_message(chat_id,
                              "̲С̲т̲р̲и̲м - ссылка на стрим\n"
                              "̲Г̲д̲е N(N - имя человека) - информация о чекточках\n"
                              "̲С̲и̲н̲и̲ч̲к̲и [N](N - количество кадров в гифке, 20 дефолт) - ссылка, снапшот и гифка\n"
                              "̲Р̲е̲г - регистрация для участия в петровиче дня\n"
                              "̲П̲е̲т̲р̲о̲в̲и̲ч̲ ̲д̲н̲я - мини-игра, определяющая кто Петрович Дня\n"
                              "̲С̲т̲а̲т̲а - статистика по Петровичам\n"
                              "̲Д̲а̲н̲е̲т - бот вернёт да или нет. Можно просто \"?\" или в конце указать \"?\"\n"
                              "̲Р̲а̲н̲д̲о̲м N[,M] (N,M - от и до) - рандомное число в заданном диапазоне\n"
                              "̲П̲о̲г̲о̲д̲а [N] (N - название города(Самара, Питер, Сызрань, Прибой)) - погода в городе\n"
                              "̲О̲б̲о̲с̲р̲а̲т̲ь [N] - рандомное оскорбление. N - что/кто либо\n"
                              "̲П̲о̲м̲о̲щ̲ь - помощь\n"
                              "\n-- команды для группы 6221 --\n"
                              "̲Р̲а̲с̲п̲и̲с̲а̲н̲и̲е - картинка с расписанием\n"
                              "̲У̲ч̲е̲б̲н̲о̲е - ссылка на папку с учебным материалом\n"
                              "̲Л̲е̲к̲ц̲и̲и - ссылка на папку с моими лекциями\n"
                              "\n--для администраторов--\n"
                              "̲У̲п̲р̲а̲в̲л̲е̲н̲и̲е (N,M) - N - chat_id, M - сообщение [Только для администраторов]\n"
                              "̲С̲т̲р̲и̲м [N] (N - ссылка на стрим) \n"


                              "\n")
        elif command in ["управление", "сообщение"]:
            if not is_lk:
                self.send_message(chat_id, "Управление ботом производится только в ЛК")
                return
            if arg is None:
                self.send_message(chat_id, "Отсутствуют аргументы chat_id и сообщение")
                return
            args = arg.split(',')
            msg_chat_id = int(args[0])
            msg = args[1]
            if not user_is_admin(user_id):
                self.send_message(chat_id, "Недостаточно прав на изменение ссылки стрима")
                return

            self.send_message(2000000000 + msg_chat_id, msg)
        elif command in ["погода"]:
            if arg is None:
                city = 'самара'
            else:
                city = arg
            from apps.API_VK.yandex_weather import get_weather

            weather = get_weather(city)

            self.send_message(chat_id, weather)
        elif command in ["обосрать"]:
            insults = ["Алик","Алкаш","алконавт","Аллаяр","Альтернативно одаренный","Амаус","Аморал","аморальный","Антихрист","Аптряй","Архаровец","Аспид","Ащеул","Баба","Баба ветрогонка","Бабашкин","Бабинский","Бабуин","Баклан","Балабол","Баламошка","Баламут","Балахвостъ","Балахрыска","Балбес","Балда","Балдабей","Баляба","Бандит","Банный лист","Баран","Бармаглот","Барнабаш","Барыга","Басалай","Басурманин","Башибузук","Без царя в голове","Бездарь","Бездельник","Безмозглая курица","Безобразник","Безпелюха","Безсоромна баба","Белебеня","Бесстыдник","Бестия","Бестолочь","Бесшабашный","Бзыря","Блаженный","Блудоумъ","Блудяшка","Бобыня","Божевольный","Божедурье","Болван","Болдырь","Болтун","Боров","Босяк","Ботаник","Брандахлыст","Бредкий","Брехло","Брехун","Брыдлый","Буня","Буслай","Быдло","Бычара","Бычьё","Бяка","В попу укушенный","Валандай","Вася  Бардуль","Вахлай","Ведьма","Веред","Верзила","Вертопрахъ","Вертухай","Вешалка","Визгопряха","Висельник","Вобла сушеная ","Волк позорный","Волки позорные","Волочайка","Волчара","Волчья сыть","Вонючка","Ворона ловить","Ворюга","Вошь на гребешке","Вшивота","Вымесок","выпивоха","Выпороток","Выродок","Вяжихвостка","Гадина","Гамадрил","Гамыра","Гандон","Гвозди","Геморрой","Гиена кладбищенская","Глазопялка","Глиста","Глиста ходячая","Глуподырый","Гнида","Гноище","Гнус","Гнусь","Говна лопата","Говно","Говноед","Голиаф","Голова садовая","Головешка с мозгами","Головка от патефона","Головорез","Голь перекатная","Гомик","Гондурас","Гонщик","Гопник","Гопота","Горилла","Горлопан","Грабастикъ","Грубиян","Грымза","Губошлёп","Гузыня","Гульня","Гусыня","Гусь","Дармоед","Дать в репу","Даун","Дебил","Дегенерат","Декадент","Демон","Дерево","Держиморда","Дерьмо","Дистрофик","Дитка","Долбень","Долботряс","Дрищь","Дрянь","Дуб","Дубина","Дубина стоеросовая","Дуботолкъ","Дундук","Дунька","Дупель","Дурак","Дуралей","дурачок","Дурбалай","Дурбецелло","Дурень","Дурилка","Дурка","Дуропляс","Дурошлеп","Дурында","Душман","Душной козел","Дятел","Егоза","Едрён батон","Ёжкин","Ёкарный бабай","Елдыга","Ёлупень","Ёнда","Ёра","Ерондер пуп","Еропка","Ерохвостъ","Ерпыль","Ершится","Етишкин дух","Жаба","Жадина","Желчный","Жердяй","Жертва аборта","Живоглот","Живодристик","Жиздоръ","Жила","Жиртрест","Жлоб","Жмот","Жополиз","Жук","Жук навозный","Жулик","Жупел","забулдыга","Загузастка","Задница","Задор","Задрот","Задрыга","Залупа","заморыш","Замухрышка","зануда","Заовинник","Зараза","засранец","Засыха","Затетёха","Захухря","заячий хвост","Звери","Зверь","Злодей","Злотвор","Злыдень","Змеиная рвота","Змея","зубоскал","Ибтую мэмэ","Идиот","Изверг","Извращенец","Изувер","Имбецил","Индюк","Ирод","Иуда","Ишак","Кабан","Каботин","Кабыздох","Каин","Какашка","Каланча","Каналья","Каракатица","Карга","Кацап","Кащей","Квазимодо","Кикимора","Киселяй","Клоп","Клубничка","Клуша","Клюшка","Кляузник","Кобель","Кобыла","Козёл","Козлодой","Козлодорасина","Козья морда","Козявка","Колдырь","Колобродъ","Коломесъ","Колотовка","Колупай","Конь педальный","Копрофаг","Копрофил","Корова","Королобый","Корявый","Косорукий","Костеря","Кочерыжка","Кошёлка","Кощей","Кракозяблик","Краля","Крамольник","Кретин","Кривляка","Криволапый","Кровопийца","Кровосос","Кропотъ","Крохобор","Крыса","Кугут","Куёлда","Курва","Куркуль","Курощупъ","Кучка на ровном месте","Кю","Лапотник","лахудра","Ледаша детина","Лежака","Леший","Липовый диплом","Лободырный","ложкомойка","лопух","лох","Лох,лохушка","Лоха","Лоший","Лудъ","Любомудръ","Лябзя","Лярва","Макака","Малахольный","Мамошка","Мандавошка","Мандуда","Маракуша","Маромойка","Мартышка","Массаракш","Мастдай однобитный","Межеумокъ","Мент","Мерзавец","Мерзопакость","Метёлка","Михрютка","Младоуменъ суще","Мозгляк","Мокрица","Мокрощёлка","Моль","Монстр","Морда","Мордоворот","Мордофиля","Моркотникъ","Москолудъ","Моська","Мочалка","Мразь","Мракобес","Мудак","Мурло","мусор","Муфлон","Мухоблудъ","Мымра","Наглец","Назойливая муха","Напыщенный индюк","Насупа","Насупоня","Нахал","Невегласъ","Невежа","Невежда","Негодяй","Негораздокъ","Недоносок","Недотёпа","Недотепа","Недотыкомка","Недоумок","Неповоротень","Непотопляемый","Несмыселъ","Нетопырь","Нефырь","Нехристь","Нечисть","Ничтожество","Обалдуй","Обдувало","Обезьяна","облезлый","Обломъ","Облудъ","Оболдуй","Оболтус","Обормот","Образина","Овца","Оглоед","Огуряла","Одоробло","Озорник","Окаёмъ","Окаянный","Околотень","Олень","Олигофрен","Олух","Олух царя небесного","омерзительный","Опущ","Орангутан","Осёл","Осиновый лист","Остолбень","Остолоп","Отморозок","Отстой","Отымалка","Охальникъ","Охламон","Очкарик","Павлин","Пакостник","паразит","Паршивец","паскуда","Пеньтюхъ","Пердимонокль","Пердун","пересмешник","Пес","петух","Пехтюкъ","Печегнётъ","Печная ездова","пигалица","Пидор","Пижон","Плеха","Поганец","Поганка","Погань","Подлец","подонок","пожиратель гравия","Позорный","попа","Попа с ручкой","Попрешница","Потаскуха","Потатуй","Похабникъ","Пресноплюй","придурок","Приставучий репей","пройдоха","Проказник","проныра","пропойца","простак","простофиля","Профура","профурсетка","прохвост","прохиндей","Прошмандовка","прощелыга","Псоватый","Пустобрёхъ","Пустошный","Пыня","Пьявка","пьянь ","Пятигузъ","Развисляй","разгильдяй","Разделать под орех","раздолбай","Раззява","разиня","Разлямзя","размазня","Разноголовый","Разтетёха","Растопча","растыка","растяпа","Расшивоха","Расщеколда","Рахубникъ","Рвань","Рогоносец","рожа","рохля","рыло","Рюма","сатрап","Свербигузка","Свинья","Сволочь","Сдёргоумка","Сексот","Секушка","Сиволапъ","Сивый мерин","Скапыжный","Скаредъ","Сквернавецъ","Скоблёное рыло","Скряга","смерд","Сняголовь","Солдафон","Стеллерова газель","Стерва","Стервец","Стиляга","Страмецъ","Страхолюдъ","Стукач","Суемудръ","сукин сын","Супостат","Сыч","Та ещё жучка","Тартыга","Тварь","Телеухъ","тетёха","Тетёшка","Титёшница","тля","Толоконный лобъ","тормоз","трепло","Трупёрда","Трутень","трынделка","Трясся","Туесъ","Тупица","тупой","Тьмонеистовый","Тюрюхайло","тюфяк","Ублюдок","Убожество","Угланъ","Удод","Упырь","Урка","Урод","Урюк","Урюпа","Ушлёпок","Фетюк","Фигляр","Филькина грамота","Фифа","Фофан","Фраер","Фуфло","Фуфлыга","хабалка","Хабалъ","халдей","Халтома","Халявщик","Хам","Хана","Хандрыга","ханыга","хапуга","Харя","Хмырь","Хмыстень","Хобяка","ходячее кладбище бифштексов","холера","холуй","Хорёк ","Хохрикъ","Хуже горькой редьки","Цуцик","Чёрт","Чёртъ верёвочный","Чувырла","Чужеядъ","Чучело","Шаврикъ","Шалава","шалопут","Шалопутъ","Шантрапа","Шаромыжник","Шваль","Шевяк","шельма","Шибздик","Шизик","Шинора","Шкура","Шлында","Шлюха","Шмакодявка","Шмара","Шмаровоз","Шпана","Шпынь голова","Шут гороховый","Шушера","Щаул","Щегол","Щенок","Юродивый","Я","Ябеда","Язва","Яйцеголовый","Яйцекладущий сын замороженного пня","Японский городовой","Ятидрёный хряп"]
            rand_int = random.randint(0, len(insults) - 1)
            if arg:
                self.send_message(chat_id,"{}, ты {}".format(arg.capitalize(),insults[rand_int].lower()))
            else:
                self.send_message(chat_id, insults[rand_int])

        #     -----------------------------------------
        elif command in ["расписание", "расп"]:
            RASP_PATH = BASE_DIR + "/static/vkapi/rasp.jpg"
            print(RASP_PATH)
            photo = self.upload.photo_messages(RASP_PATH)[0]
            attachments.append('photo{}_{}'.format(photo['owner_id'], photo['id']))
            self.send_message(chat_id, "", attachments=attachments)
        elif command in ["гугл", "ссылка", "учебное"]:
            self.send_message(chat_id, "https://drive.google.com/open?id=1AJPnT2XXYNc39-2CSr_MzHnv4hs6Use6")
        elif command in ["лекции"]:
            self.send_message(chat_id, "https://drive.google.com/open?id=19QVRRbj6ePEFTxS2bHOjjaKljkJwZxNB")
        else:
            self.send_message(chat_id, "Я не понял команды \"%s\"" % command)

    def __init__(self):
        super().__init__()
        f = open(BASE_DIR + "/secrets/vk.txt", "r")
        self._TOKEN = f.readline().strip()
        self._group_id = int(f.readline().strip())
        vk_session = vk_api.VkApi(token=self._TOKEN)
        self.longpoll = MyVkBotLongPoll(vk_session, group_id=self._group_id)
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
                    if message_for_me(message, self.mentions) or event.object.peer_id == event.object.from_id or \
                            message[0] == '/':
                        full_message = message

                        if message[0] == '/':
                            message = message[1:]

                        message = parse_msg_to_me(message, self.mentions)
                        message = parse_msg(message)
                        self.menu(event.object.peer_id,
                                  event.object.from_id,
                                  message['COMMAND'],
                                  message['ARG'],
                                  event.object.peer_id == event.object.from_id,
                                  full_message)
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

    def set_chat_title_if_not_equals(self, chat_id, title):
        if title != self.vk.messages.getConversationsById(peer_ids=2000000000 + chat_id)['items'][0]['chat_settings'][
            'title']:
            self.vk.messages.editChat(chat_id=chat_id, title=title)
            print('set title to', title)
        else:
            print('dont set title')


class MyVkBotLongPoll(VkBotLongPoll):
    def listen(self):
        while True:
            try:
                for event in self.check():
                    yield event
            except Exception as e:
                print('ОШИБКА ВЫПОЛНЕНИЯ ЛОНГПОЛА 2:', e)
