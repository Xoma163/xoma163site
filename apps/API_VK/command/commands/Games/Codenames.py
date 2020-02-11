# ToDo: возможно в будущем связать CodenamesUser и CodenamesSession

import json
import random
from threading import Lock

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.games.models import CodenamesUser, CodenamesSession

lock = Lock()

MIN_USERS = 4
DIMENSION = 5

WORDS = ['Австралия', 'Автомат', 'Агент', 'Адвокат', 'Азия', 'Акт', 'Альбом', 'Альпы', 'Америка', 'Амфибия', 'Ангел',
         'Англия', 'Антарктида', 'Аппарат', 'Атлантида', 'Африка', 'Ацтек', 'Бабочка', 'База', 'Байкал', 'Банк', 'Баня',
         'Бар', 'Барьер', 'Бассейн', 'Батарея', 'Башня', 'Берёза', 'Берлин', 'Бермуды', 'Билет', 'Биржа', 'Блин',
         'Блок', 'Боевик', 'Бокс', 'Болезнь', 'Больница', 'Бомба', 'Боров', 'Борт', 'Ботинок', 'Бочка', 'Брак',
         'Бревно', 'Бумага', 'Бутылка', 'Бык', 'Вагон', 'Вал', 'Ведьма', 'Век', 'Венец', 'Вертолёт', 'Верфь', 'Вес',
         'Ветер', 'Взгляд', 'Вид', 'Вилка', 'Вирус', 'Вода', 'Водолаз', 'Вождь', 'Воздух', 'Война', 'Волна', 'Вор',
         'Время', 'Высота', 'Газ', 'Галоп', 'Гвоздь', 'Гений', 'Германия', 'Гигант', 'Глаз', 'Голливуд', 'Голова',
         'Горло', 'Горн', 'Гранат', 'Гребень', 'Греция', 'Гриф', 'Груша', 'Дама', 'Декрет', 'День', 'Десна', 'Динозавр',
         'Диск', 'Доктор', 'Дракон', 'Дробь', 'Дума', 'Дух', 'Дыра', 'Дятел', 'Европа', 'Египет', 'Единорог', 'Ёрш',
         'Жизнь', 'Жила', 'Жук', 'Журавль', 'Залог', 'Замок', 'Заноза', 'Запад', 'Запах', 'Заяц', 'Звезда', 'Зебра',
         'Земля', 'Знак', 'Золото', 'Зона', 'Зуб', 'Игла', 'Игра', 'Икра', 'Индия', 'Институт', 'Кабинет', 'Кавалер',
         'Кадр', 'Казино', 'Камень', 'Камера', 'Канал', 'Караул', 'Карлик', 'Карта', 'Каша', 'Кенгуру', 'Кентавр',
         'Кетчуп', 'Киви', 'Кисть', 'Кит', 'Китай', 'Клетка', 'Ключ', 'Кокетка', 'Кол', 'Колода', 'Колонна', 'Кольцо',
         'Команда', 'Конёк', 'Контрабандист', 'Концерт', 'Кора', 'Корабль', 'Королева', 'Король', 'Корона', 'Коса',
         'Кость', 'Косяк', 'Кошка', 'Край', 'Кран', 'Крест', 'Кролик', 'Крошка', 'Круг', 'Крыло', 'Кулак', 'Курс',
         'Лад', 'Лазер', 'Лама', 'Ласка', 'Лев', 'Лёд', 'Лейка', 'Лес', 'Лимузин', 'Линия', 'Липа', 'Лист', 'Лицо',
         'Ложе', 'Лондон', 'Лошадь', 'Лук', 'Луна', 'Луч', 'Масло', 'Масса', 'Мат', 'Машина', 'Мёд', 'Медведь',
         'Мексика', 'Мелочь', 'Место', 'Механизм', 'Микроскоп', 'Миллионер', 'Мир', 'Морковь', 'Мороженое', 'Москва',
         'Мост', 'Мотив', 'Мушка', 'Мышь', 'Налёт', 'Наряд', 'Небоскрёб', 'Ниндзя', 'Нож', 'Номер', 'Норка', 'Нота',
         'Ночь', 'Нью-йорк', 'Няня', 'Область', 'Облом', 'Образ', 'Образование', 'Обрез', 'Овсянка', 'Огонь', 'Олимп',
         'Опера', 'Операция', 'Орган', 'Орёл', 'Осьминог', 'Отель', 'Падение', 'Палата', 'Палец', 'Палочка', 'Панель',
         'Пара', 'Парашют', 'Парк', 'Партия', 'Пассаж', 'Паук', 'Пачка', 'Пекин', 'Перевод', 'Перемена', 'Перо',
         'Перчатка', 'Пилот', 'Пингвин', 'Пирамида', 'Пират', 'Пистолет', 'Плата', 'Платье', 'Площадь', 'Пляж', 'Побег',
         'Повар', 'Подкова', 'Подъём', 'Покров', 'Пол', 'Поле', 'Полис', 'Полиция', 'Помёт', 'Порода', 'Посольство',
         'Поток', 'Почка', 'Пояс', 'Право', 'Предложение', 'Предприниматель', 'Прибор', 'Привод', 'Призрак',
         'Принцесса', 'Пришелец', 'Пробка', 'Проводник', 'Проказа', 'Прокат', 'Проспект', 'Профиль', 'Путь', 'Пушкин',
         'Развод', 'Разворот', 'Рак', 'Раковина', 'Раствор', 'Рейд', 'Рим', 'Робот', 'Рог', 'Род', 'Рок', 'Рубашка',
         'Рукав', 'Рулетка', 'Рыба', 'Рысь', 'Рыцарь', 'Салют', 'Сантехник', 'Сатурн', 'Свет', 'Свидетель', 'Секрет',
         'Секция', 'Сердце', 'Сеть', 'Сила', 'Скат', 'Смерть', 'Снаряд', 'Снег', 'Снеговик', 'Собака', 'Совет',
         'Солдат', 'Соль', 'Состав', 'Спутник', 'Среда', 'Ссылка', 'Стадион', 'Стан', 'Станок', 'Ствол', 'Стекло',
         'Стена', 'Стойка', 'Стол', 'Стопа', 'Стрела', 'Строй', 'Струна', 'Стул', 'Ступень', 'Судьба', 'Супергерой',
         'Такса', 'Танец', 'Тарелка', 'Театр', 'Телескоп', 'Течение', 'Титан', 'Токио', 'Точка', 'Трава', 'Треугольник',
         'Труба', 'Туба', 'Тур', 'Ударник', 'Удел', 'Узел', 'Урал', 'Урна', 'Утка', 'Утконос', 'Учёный', 'Учитель',
         'Факел', 'Фаланга', 'Фига', 'Флейта', 'Фокус', 'Форма', 'Франция', 'Хвост', 'Хлопок', 'Центр', 'Церковь',
         'Частица', 'Червь', 'Шар', 'Шоколад', 'Шпагат', 'Шпион', 'Штат', 'Шуба', 'Экран', 'Эльф', 'Эфир', 'Юпитер',
         'Яблоко', 'Яд', 'Язык', 'Якорь', 'Ясли']

translator = {
    'red': 'красная команда',
    'blue': 'синяя команда',
    'red_wait': 'капитан красной команды',
    'blue_wait': 'капитан синей команы',
}

translator_commands = {
    'red': 'красной',
    'blue': 'синей'
}


def check_player_captain(player):
    if player.role == 'captain':
        return True
    raise RuntimeError("Загадывать может только капитан")


def check_next_step(session, step_name):
    if session.next_step == step_name:
        return True

    raise RuntimeError("Сейчас не ваш ход")


def check_player(player):
    if player:
        return True
    raise RuntimeError("Вы не игрок")


def check_session(session):
    if session:
        return True
    raise RuntimeError("Игра ещё не началась")


def check_not_session(session):
    if not session:
        return True
    raise RuntimeError("Игра уже началась")


def get_another_command(command):
    if command == 'red':
        return 'blue'
    elif command == 'blue':
        return 'red'


class Codenames(CommonCommand):
    def __init__(self):
        names = ["коднеймс", "codenames", "кн", "км"]
        help_text = "Коднеймс - игра коднеймс"
        detail_help_text = "Коднеймс - игра коднеймс.\n" \
                           "Правила: https://ru.wikipedia.org/wiki/Codenames\n\n" \
                           "Коднеймс рег - регистрация в игре\n" \
                           "Коднеймс дерег - дерегистрация в игре\n" \
                           "Коднеймс старт - старт игры\n" \
                           "Коднеймс клава - текущая клавиатура игры\n" \
                           "Коднеймс инфо - команды, кол-во слов, чей ход, загаданное слово\n" \
                           "Коднеймс загадать (N,M) - N - количество слов, M - загадываемое слово, \n" \
                           "Угадывание происходит путём нажатия на кнопки"
        super().__init__(names, help_text, detail_help_text)

    def init_var(self):

        if self.vk_event.from_chat:
            self.session = CodenamesSession.objects.filter(chat=self.vk_event.chat).first()
            self.players = CodenamesUser.objects.filter(chat=self.vk_event.chat)
            self.player = self.players.filter(user=self.vk_event.sender).first()
            self.players_captains = self.players.filter(role='captain')
        elif self.vk_event.from_user:
            self.player = CodenamesUser.objects.filter(user=self.vk_event.sender).first()
            chat = self.player.chat
            self.session = CodenamesSession.objects.filter(chat=chat).first()
            self.players = CodenamesUser.objects.filter(chat=chat)
            self.players_captains = self.players.filter(role='captain')

    def start(self):
        with lock:
            self.init_var()

            if self.vk_event.args:
                if self.vk_event.args[0].lower() in ['рег', 'регистрация']:
                    check_not_session(self.session)
                    if len(CodenamesUser.objects.filter(chat=self.vk_event.chat, user=self.vk_event.sender)) > 0:
                        return 'Ты уже зарегистрирован'
                    if len(CodenamesUser.objects.filter(user=self.vk_event.sender)) > 0:
                        return 'Нельзя участвовать сразу в двух играх'
                    codenames_user = CodenamesUser()
                    codenames_user.user = self.vk_event.sender
                    codenames_user.chat = self.vk_event.chat
                    codenames_user.save()

                    codenames_users_list = [str(player.user) for player in self.players]
                    codenames_users_str = "\n".join(codenames_users_list)

                    return "Зарегистрировал. Сейчас зарегистрированы:\n" \
                           f"{codenames_users_str}\n"
                if self.vk_event.args[0].lower() in ['дерег']:
                    check_not_session(self.session)
                    self.player.delete()

                    codenames_users_list = [str(player.user) for player in self.players]
                    codenames_users_str = "\n".join(codenames_users_list)

                    # ToDo: возможно здесь вывод пользователя будет, надо заново
                    return "Дерегнул. Сейчас зарегистрированы:\n" \
                           f"{codenames_users_str}\n"
                elif self.vk_event.args[0].lower() in ['старт']:
                    self.check_conversation()
                    check_not_session(self.session)

                    codenames_users_list = [str(player.user) for player in self.players]
                    codenames_users_str = "\n".join(codenames_users_list)
                    if len(self.players) < MIN_USERS:
                        return f"Минимальное количество игроков - {MIN_USERS}. Сейчас зарегистрированы:\n" \
                               f"{codenames_users_str}"

                    self.prepare_game()
                    return
                elif self.vk_event.args[0].lower() in ['загадать']:
                    check_session(self.session)
                    check_player(self.player)
                    self.check_pm()
                    check_player_captain(self.player)
                    command = self.player.command
                    check_next_step(self.session, command + "_wait")
                    if len(self.vk_event.args) < 3:
                        return "Недостаточно аргументов"
                    self.int_args = [1]
                    self.parse_int_args()

                    count = int(self.vk_event.args[1])
                    if count > 9:
                        count = 9
                    elif count < 1:
                        return "Число загадываемых слов не может быть меньше 1"
                    word = self.vk_event.args[2]
                    self.do_the_riddle(command, count, word)
                    return 'Отправил в конфу'
                elif self.vk_event.payload:
                    check_session(self.session)
                    self.check_conversation()
                    check_player(self.player)
                    if self.vk_event.payload['args']['action'] in ['слово']:
                        if self.player.role == 'captain':
                            return "Капитан не может угадывать"
                        if self.vk_event.payload['args']['state'] == 'open':
                            return "Слово уже открыто"
                        check_next_step(self.session, self.player.command)

                        self.select_word(self.vk_event.payload['args']['row'], self.vk_event.payload['args']['col'])
                        return
                    return "Внутренняя ошибка. Неизвестный action в payload"
                elif self.vk_event.args[0].lower() in ['клава']:
                    check_session(self.session)
                    check_player(self.player)
                    board = json.loads(self.session.board)
                    user_is_captain = self.player.role == 'captain'
                    if user_is_captain:
                        if self.vk_event.from_chat:
                            self.send_keyboard(board)
                        else:
                            self.check_pm()
                            self.send_captain_keyboard(board)
                    else:
                        self.check_conversation()
                        self.send_keyboard(board)
                    return
                elif self.vk_event.args[0].lower() in ['инфо', 'инфа', 'информация']:
                    check_session(self.session)
                    self.check_conversation()

                    msg = self.get_info()
                    return msg
                else:
                    return "Не знаю такого аргумента. /ман коднеймс"
            # Регистрация
            else:
                return 'Не переданы аргументы. /ман коднеймс'

            return 'Как ты сюда попал?'

    # Подготовка и старт игры
    def prepare_game(self):

        def get_random_words():
            words_shuffled = sorted(WORDS, key=lambda x: random.random())[:DIMENSION * DIMENSION]
            team_words_shuffled = []
            for i, word in enumerate(words_shuffled):
                team_words_shuffled.append(
                    {'state': 'close', 'name': word})
                if i < 9:
                    team_words_shuffled[-1]['type'] = 'blue'
                elif i == 9:
                    team_words_shuffled[-1]['type'] = 'death'
                elif i < 18:
                    team_words_shuffled[-1]['type'] = 'red'
                else:
                    team_words_shuffled[-1]['type'] = 'neutral'

            team_words_shuffled = sorted(team_words_shuffled, key=lambda x: random.random())
            for i, word in enumerate(team_words_shuffled):
                team_words_shuffled[i]['row'] = int(i / DIMENSION)
                team_words_shuffled[i]['col'] = i % DIMENSION
            words_table = []
            for i in range(DIMENSION):
                words_table.append(team_words_shuffled[i * DIMENSION:(i + 1) * DIMENSION])

            return words_table

        def set_commands(codenames_users):
            def set_team(team, color):
                for codenames_user in team:
                    codenames_user.command = color
                    codenames_user.save()

            def set_captain(team):
                team[0].role = 'captain'
                team[0].save()

            codenames_users_shuffled = sorted(codenames_users, key=lambda x: random.random())

            half_users = int(len(codenames_users_shuffled) / 2)
            if len(codenames_users_shuffled) % 2 == 1:
                half_users += 1

            blue_team = codenames_users_shuffled[:half_users]
            red_team = codenames_users_shuffled[half_users:]

            set_team(blue_team, 'blue')
            set_team(red_team, 'red')

            set_captain(blue_team)
            set_captain(red_team)

        set_commands(self.players)

        board = get_random_words()

        session = CodenamesSession()
        session.chat = self.vk_event.chat
        session.board = json.dumps(board)
        session.save()
        self.session = session

        self.send_keyboard(board)
        self.vk_bot.send_message(self.vk_event.peer_id, msg=self.get_info())

        for captain in self.players_captains:
            self.send_captain_keyboard(board, captain)

    # Тык игрока
    def select_word(self, row, col):
        board = json.loads(self.session.board)

        command = self.player.command
        another_command = get_another_command(command)
        selected_word = board[row][col]
        selected_word['state'] = 'open'

        if selected_word['type'] == command:
            self.session.count -= 1

            if self.session.count == 0:
                self.session.next_step = f"{another_command}_wait"
                self.vk_bot.send_message(self.session.chat.chat_id,
                                         f"Угадали!\nПередаём ход капитану {translator_commands[another_command]} команды ")

                another_captain = self.players_captains.filter(command=another_command).first()
                self.send_captain_keyboard(board, another_captain)

            else:
                self.vk_bot.send_message(self.session.chat.chat_id,
                                         f"Угадали!\nПродолжайте угадывать")
            self.session.board = json.dumps(board)
            self.session.save()
        elif selected_word['type'] == another_command or selected_word['type'] == 'neutral':
            self.session.next_step = f"{another_command}_wait"
            self.session.board = json.dumps(board)
            self.session.save()

            self.vk_bot.send_message(self.session.chat.chat_id,
                                     f"Не угадали :(\nПередаём ход капитану {translator_commands[another_command]} команды")
            another_captain = self.players_captains.filter(command=another_command).first()
            self.send_captain_keyboard(board, another_captain)

        elif selected_word['type'] == 'death':
            self.vk_bot.send_message(self.session.chat.chat_id, f"Смэрт")
            self.game_over(winner=another_command)
            return

        is_game_over = self.check_game_over(board)
        if is_game_over:
            self.game_over(is_game_over)
            return

        self.send_keyboard(board)

    # Загадка капитана
    def do_the_riddle(self, command, count, word):

        self.vk_bot.send_message(self.session.chat.chat_id,
                                 f"Капитан {translator_commands[command]} команды:\n{count} - {word}")

        self.session.next_step = command
        self.session.count = count
        self.session.word = word
        self.session.save()

        board = json.loads(self.session.board)
        self.send_keyboard(board)

    # Метод получает количество оставшихся закрытых слов команд
    @staticmethod
    def get_team_words(board):
        words = {'red': 0, 'blue': 0}
        for row in board:
            for elem in row:
                if elem['state'] == 'close':
                    if elem['type'] == 'red' or elem['type'] == 'blue':
                        words[elem['type']] += 1
        return words

    # Проверка на конец игры
    def check_game_over(self, board):
        team_words = self.get_team_words(board)

        if team_words['red'] == 0:
            return 'red'
        elif team_words['blue'] == 0:
            return 'blue'
        else:
            return None

    # Конец игры
    def game_over(self, winner):
        from apps.API_VK.command import EMPTY_KEYBOARD

        self.vk_bot.send_message(self.session.chat.chat_id,
                                 f'Игра закончена.\nПобеда {translator_commands[winner]} команды',
                                 keyboard=EMPTY_KEYBOARD)

        self.session.delete()
        self.players.delete()

    def get_info(self):
        def get_commands():
            def get_command_msg(command_name, command_players):
                team_msg = f"{translator[command_name].capitalize()}:\n"
                for player in command_players:
                    if player.role == 'captain':
                        team_msg += f'{player} - Капитан\n'
                    else:
                        team_msg += f'{player}\n'
                return team_msg + "\n\n"

            commands = {'red': [], 'blue': []}
            commands_msg = {'red': None, 'blue': None}
            for player in self.players:
                commands[player.command].append(player)
            for command in commands:
                commands_msg[command] = get_command_msg(command, commands[command])

            return commands_msg

        commands_colors = ['blue', 'red']

        commands = get_commands()

        board = json.loads(self.session.board)
        words_left = self.get_team_words(board)

        riddle = None
        if self.session.next_step == 'red' or self.session.next_step == 'blue':
            riddle = f"{translator[self.session.next_step + '_wait'].capitalize()}:\n{self.session.count} - {self.session.word}"

        step = f'Сейчас ходит {translator[self.session.next_step]}'

        spacer = "-----------------------------------------------------------"
        total_msg = ""
        for command in commands_colors:
            total_msg += f"{commands[command]}\n" \
                         f"Осталось слов - {words_left[command]}\n{spacer}\n"
        total_msg += step + f"\n{spacer}\n"
        if riddle:
            total_msg += riddle
        return total_msg

    # Работа с клавиатурами
    @staticmethod
    # Врап элемента клавиатуры
    def get_elem(elem, for_captain=False):

        def get_color():
            if for_captain:
                captain_color_translate = {
                    'red': 'negative',
                    'death': 'positive',
                    'blue': 'primary',
                    'neutral': 'secondary'
                }
                return captain_color_translate[elem['type']]
            else:
                color_translate = {'close': {
                    'red': 'secondary',
                    'death': 'secondary',
                    'blue': 'secondary',
                    'neutral': 'secondary'
                },
                    'open': {
                        'red': 'negative',
                        'death': 'positive',
                        'blue': 'primary',
                        'neutral': 'secondary'
                    }
                }
                return color_translate[elem['state']][elem['type']]

        def get_name():
            name_translate = {
                'open': "".join(["ᅠ" for i in range(2)]),
                'close': elem['name']
            }
            return name_translate[elem['state']]

        return {
            "action": {
                "type": "text",
                "label": get_name(),
                "payload": json.dumps({
                    "command": "коднеймс",
                    "args": {
                        "action": 'слово',
                        'row': elem['row'],
                        "col": elem['col'],
                        "state": elem['state']
                    }},
                    ensure_ascii=False)
            },
            "color": get_color()
        }

    # Клава для вывода в линию
    def get_inline_keyboard(self, table, for_captain=False):
        keyboards = []

        for i, row in enumerate(table):
            rows = []
            for j, elem in enumerate(row):
                rows.append(self.get_elem(elem, for_captain))

            keyboards.append({
                "one_time": False,
                "buttons": [rows],
                "inline": True,
            })
        return keyboards

    # Обычная клава
    def get_keyboard(self, table, for_captain=False):
        buttons = []
        for i, row in enumerate(table):
            rows = []
            for j, elem in enumerate(row):
                rows.append(self.get_elem(elem, for_captain))
            buttons.append(rows)

        keyboard = {
            "one_time": False,
            "buttons": buttons,
        }
        return keyboard

    def send_keyboard(self, board):
        keyboard = self.get_keyboard(board)
        self.vk_bot.send_message(self.session.chat.chat_id, msg="&#13;", keyboard=keyboard)

        keyboards = self.get_inline_keyboard(board)
        for keyboard in keyboards:
            labels = [button['action']['label'] for button in keyboard['buttons'][0]]
            keyboard_str = ", ".join(labels)
            self.vk_bot.send_message(self.session.chat.chat_id, msg=keyboard_str, keyboard=keyboard)

    def send_captain_keyboard(self, board, captain=None):
        if captain:
            peer_id = captain.user.user_id
        else:
            peer_id = self.vk_event.peer_id

        keyboard = self.get_keyboard(board, for_captain=True)
        self.vk_bot.send_message(peer_id, msg="&#13;", keyboard=keyboard)

        keyboards = self.get_inline_keyboard(board, for_captain=True)

        for keyboard in keyboards:
            labels = [button['action']['label'] for button in keyboard['buttons'][0]]
            keyboard_str = ", ".join(labels)
            self.vk_bot.send_message(peer_id, msg=keyboard_str, keyboard=keyboard)
