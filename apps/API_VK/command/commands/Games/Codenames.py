# import json
# from threading import Lock
#
# from apps.API_VK.command.CommonCommand import CommonCommand
# from apps.games.models import CodenamesUser
#
# lock = Lock()
#
# MIN_USERS = 2
# DIMENSION = 5
#
# WORDS = ['Австралия', 'Автомат', 'Агент', 'Адвокат', 'Азия', 'Акт', 'Альбом', 'Альпы', 'Америка', 'Амфибия', 'Ангел',
#          'Англия', 'Антарктида', 'Аппарат', 'Атлантида', 'Африка', 'Ацтек', 'Бабочка', 'База', 'Байкал', 'Банк', 'Баня',
#          'Бар', 'Барьер', 'Бассейн', 'Батарея', 'Башня', 'Берёза', 'Берлин', 'Бермуды', 'Билет', 'Биржа', 'Блин',
#          'Блок', 'Боевик', 'Бокс', 'Болезнь', 'Больница', 'Бомба', 'Боров', 'Борт', 'Ботинок', 'Бочка', 'Брак',
#          'Бревно', 'Бумага', 'Бутылка', 'Бык', 'Вагон', 'Вал', 'Ведьма', 'Век', 'Венец', 'Вертолёт', 'Верфь', 'Вес',
#          'Ветер', 'Взгляд', 'Вид', 'Вилка', 'Вирус', 'Вода', 'Водолаз', 'Вождь', 'Воздух', 'Война', 'Волна', 'Вор',
#          'Время', 'Высота', 'Газ', 'Галоп', 'Гвоздь', 'Гений', 'Германия', 'Гигант', 'Глаз', 'Голливуд', 'Голова',
#          'Горло', 'Горн', 'Гранат', 'Гребень', 'Греция', 'Гриф', 'Груша', 'Дама', 'Декрет', 'День', 'Десна', 'Динозавр',
#          'Диск', 'Доктор', 'Дракон', 'Дробь', 'Дума', 'Дух', 'Дыра', 'Дятел', 'Европа', 'Египет', 'Единорог', 'Ёрш',
#          'Жизнь', 'Жила', 'Жук', 'Журавль', 'Залог', 'Замок', 'Заноза', 'Запад', 'Запах', 'Заяц', 'Звезда', 'Зебра',
#          'Земля', 'Знак', 'Золото', 'Зона', 'Зуб', 'Игла', 'Игра', 'Икра', 'Индия', 'Институт', 'Кабинет', 'Кавалер',
#          'Кадр', 'Казино', 'Камень', 'Камера', 'Канал', 'Караул', 'Карлик', 'Карта', 'Каша', 'Кенгуру', 'Кентавр',
#          'Кетчуп', 'Киви', 'Кисть', 'Кит', 'Китай', 'Клетка', 'Ключ', 'Кокетка', 'Кол', 'Колода', 'Колонна', 'Кольцо',
#          'Команда', 'Конёк', 'Контрабандист', 'Концерт', 'Кора', 'Корабль', 'Королева', 'Король', 'Корона', 'Коса',
#          'Кость', 'Косяк', 'Кошка', 'Край', 'Кран', 'Крест', 'Кролик', 'Крошка', 'Круг', 'Крыло', 'Кулак', 'Курс',
#          'Лад', 'Лазер', 'Лама', 'Ласка', 'Лев', 'Лёд', 'Лейка', 'Лес', 'Лимузин', 'Линия', 'Липа', 'Лист', 'Лицо',
#          'Ложе', 'Лондон', 'Лошадь', 'Лук', 'Луна', 'Луч', 'Масло', 'Масса', 'Мат', 'Машина', 'Мёд', 'Медведь',
#          'Мексика', 'Мелочь', 'Место', 'Механизм', 'Микроскоп', 'Миллионер', 'Мир', 'Морковь', 'Мороженое', 'Москва',
#          'Мост', 'Мотив', 'Мушка', 'Мышь', 'Налёт', 'Наряд', 'Небоскрёб', 'Ниндзя', 'Нож', 'Номер', 'Норка', 'Нота',
#          'Ночь', 'Нью-йорк', 'Няня', 'Область', 'Облом', 'Образ', 'Образование', 'Обрез', 'Овсянка', 'Огонь', 'Олимп',
#          'Опера', 'Операция', 'Орган', 'Орёл', 'Осьминог', 'Отель', 'Падение', 'Палата', 'Палец', 'Палочка', 'Панель',
#          'Пара', 'Парашют', 'Парк', 'Партия', 'Пассаж', 'Паук', 'Пачка', 'Пекин', 'Перевод', 'Перемена', 'Перо',
#          'Перчатка', 'Пилот', 'Пингвин', 'Пирамида', 'Пират', 'Пистолет', 'Плата', 'Платье', 'Площадь', 'Пляж', 'Побег',
#          'Повар', 'Подкова', 'Подъём', 'Покров', 'Пол', 'Поле', 'Полис', 'Полиция', 'Помёт', 'Порода', 'Посольство',
#          'Поток', 'Почка', 'Пояс', 'Право', 'Предложение', 'Предприниматель', 'Прибор', 'Привод', 'Призрак',
#          'Принцесса', 'Пришелец', 'Пробка', 'Проводник', 'Проказа', 'Прокат', 'Проспект', 'Профиль', 'Путь', 'Пушкин',
#          'Развод', 'Разворот', 'Рак', 'Раковина', 'Раствор', 'Рейд', 'Рим', 'Робот', 'Рог', 'Род', 'Рок', 'Рубашка',
#          'Рукав', 'Рулетка', 'Рыба', 'Рысь', 'Рыцарь', 'Салют', 'Сантехник', 'Сатурн', 'Свет', 'Свидетель', 'Секрет',
#          'Секция', 'Сердце', 'Сеть', 'Сила', 'Скат', 'Смерть', 'Снаряд', 'Снег', 'Снеговик', 'Собака', 'Совет',
#          'Солдат', 'Соль', 'Состав', 'Спутник', 'Среда', 'Ссылка', 'Стадион', 'Стан', 'Станок', 'Ствол', 'Стекло',
#          'Стена', 'Стойка', 'Стол', 'Стопа', 'Стрела', 'Строй', 'Струна', 'Стул', 'Ступень', 'Судьба', 'Супергерой',
#          'Такса', 'Танец', 'Тарелка', 'Театр', 'Телескоп', 'Течение', 'Титан', 'Токио', 'Точка', 'Трава', 'Треугольник',
#          'Труба', 'Туба', 'Тур', 'Ударник', 'Удел', 'Узел', 'Урал', 'Урна', 'Утка', 'Утконос', 'Учёный', 'Учитель',
#          'Факел', 'Фаланга', 'Фига', 'Флейта', 'Фокус', 'Форма', 'Франция', 'Хвост', 'Хлопок', 'Центр', 'Церковь',
#          'Частица', 'Червь', 'Шар', 'Шоколад', 'Шпагат', 'Шпион', 'Штат', 'Шуба', 'Экран', 'Эльф', 'Эфир', 'Юпитер',
#          'Яблоко', 'Яд', 'Язык', 'Якорь', 'Ясли']
#
#
# class Codenames(CommonCommand):
#     def __init__(self):
#         names = ["коднеймс", "codenames"]
#         help_text = "Коднеймс - игра коднеймс"
#         detail_help_text = "Коднеймс - ToDo:"
#         super().__init__(names, help_text, detail_help_text, conversation=True)
#
#     def start(self):
#         with lock:
#
#             if self.vk_event.args:
#                 if self.vk_event.args[0].lower() in ['старт']:
#                     codenames_users = CodenamesUser.objects.filter(chat=self.vk_event.chat)
#
#                     codenames_users_list = [str(codenames_user.user) for codenames_user in codenames_users]
#                     codenames_users_str = "\n".join(codenames_users_list)
#                     if len(codenames_users) < MIN_USERS:
#                         return f"Нужно хотя бы 4 игрока. Сейчас зарегистрированы:\n" \
#                                f"{codenames_users_str}"
#
#                     self.prepare_game(codenames_users)
#                     return 'ok'
#
#             else:
#                 if len(CodenamesUser.objects.filter(chat=self.vk_event.chat, user=self.vk_event.sender)) > 0:
#                     return 'Ты уже зарегистрирован!'
#
#                 codenames_user = CodenamesUser()
#                 codenames_user.user = self.vk_event.sender
#                 codenames_user.chat = self.vk_event.chat
#                 codenames_user.save()
#                 return "Зарегистрировал"
#
#         return 'test'
#
#     def prepare_game(self, codenames_users):
#
#         def set_team(team, color):
#             for codenames_user in team:
#                 codenames_user.command = color
#                 codenames_user.save()
#
#         def set_captain(team):
#             team[0].role = 'captain'
#             team[0].save()
#
#         def get_random_words():
#             words_shuffled = sorted(WORDS, key=lambda x: random.random())[:DIMENSION * DIMENSION]
#
#             words_table = []
#             words_str = ""
#             for i in range(DIMENSION):
#                 words_table.append(words_shuffled[i * DIMENSION:(i + 1) * DIMENSION])
#                 words_str += "\n" + (" ".join(words_table[-1]))
#             self.vk_bot.send_message(self.vk_event.peer_id, words_str)
#
#             return words_table
#
#         import random
#         codenames_users_shuffled = sorted(codenames_users, key=lambda x: random.random())
#
#         half_users = int(len(codenames_users_shuffled) / 2)
#
#         blue_team = codenames_users_shuffled[:half_users]
#         red_team = codenames_users_shuffled[half_users:]
#
#         set_team(blue_team, 'blue')
#         set_team(red_team, 'red')
#
#         set_captain(blue_team)
#         set_captain(red_team)
#
#         random_words = get_random_words()
#         keyboard = self.get_keyboard(random_words)
#
#         self.vk_bot.send_message(self.vk_event.peer_id, 'Слова', keyboard=keyboard)
#
#     def get_keyboard(self, table):
#
#         def wrap_elem(elem):
#             return {
#                 "action": {
#                     "type": "text",
#                     "label": elem,
#                     "payload": json.dumps({"command": "коднеймс", "args": {"word": elem}}, ensure_ascii=False)
#                 },
#                 "color": "secondary"
#             }
#
#         buttons = []
#         for i, row in enumerate(table):
#             rows = []
#             for j, elem in enumerate(row):
#                 rows.append(wrap_elem(elem))
#             buttons.append(rows)
#
#         keyboard = {
#             "one_time": False,
#             "buttons": buttons,
#             # "inline": True,
#         }
#         return keyboard
