def get_keyboard(is_admin=False, is_moderator=False, is_student=False):
    buttons = []
    if is_admin:
        buttons += get_admin_keyboard_buttons()
    if is_moderator:
        buttons += get_modetaror_keyboard_buttons()
    if is_student:
        buttons += get_student_keyboard_buttons()
    buttons += get_default_keyboard_buttons()

    keyboard = {
        "one_time": False,
        "buttons": buttons
    }
    return keyboard


def get_admin_keyboard_buttons():
    buttons = [
        [
            {
                "action": {
                    "type": "text",
                    "label": "Старт"
                },
                "color": "positive"
            },
            {
                "action": {
                    "type": "text",
                    "label": "Стоп"
                },
                "color": "negative"
            },
            {
                "action": {
                    "type": "text",
                    "label": "Старт синички"
                },
                "color": "positive"
            },
            {
                "action": {
                    "type": "text",
                    "label": "Стоп синички"
                },
                "color": "negative"
            }
        ],
    ]
    return buttons


def get_modetaror_keyboard_buttons():
    buttons = [
        [
            {
                "action": {
                    "type": "text",
                    "label": "Логи"
                },
                "color": "primary"
            }
        ],
    ]
    return buttons


def get_default_keyboard_buttons():
    buttons = [
        [
            {
                "action": {
                    "type": "text",
                    "label": "Погода"
                },
                "color": "primary"
            },
            {
                "action": {
                    "type": "text",
                    "label": "Помощь"
                },
                "color": "primary"
            }
        ],
        [
            {
                "action": {
                    "type": "text",
                    "label": "Синички 0"
                },
                "color": "primary"
            },
            {
                "action": {
                    "type": "text",
                    "label": "Синички 20"
                },
                "color": "primary"
            },
            {
                "action": {
                    "type": "text",
                    "label": "Синички 100"
                },
                "color": "primary"
            }
        ],
        [
            {
                "action": {
                    "type": "text",
                    "label": "Скрыть"
                },
                "color": "secondary"
            }
        ],
    ]
    return buttons


def get_student_keyboard_buttons():
    buttons = [
        [
            {
                "action": {
                    "type": "text",
                    "label": "Расписание"
                },
                "color": "primary"
            },
            {
                "action": {
                    "type": "text",
                    "label": "Неделя"
                },
                "color": "primary"
            },
            {
                "action": {
                    "type": "text",
                    "label": "Учебное"
                },
                "color": "primary"
            },
            {
                "action": {
                    "type": "text",
                    "label": "Лекции"
                },
                "color": "primary"
            }
        ],
    ]
    return buttons


def get_help_text(is_admin, is_student):
    help_text = ""

    default_help = \
        "̲С̲т̲р̲и̲м - ссылка на стрим\n" \
        "̲Г̲д̲е N(N - имя человека) - информация о чекточках\n" \
        "̲С̲и̲н̲и̲ч̲к̲и [N[,M]](N - количество кадров в гифке, 20 дефолт, M - качество(0 или 1), 0 дефолт) - ссылка, снапшот и гифка\n" \
        "̲Р̲е̲г - регистрация для участия в петровиче дня\n" \
        "̲П̲е̲т̲р̲о̲в̲и̲ч̲ ̲д̲н̲я - мини-игра, определяющая кто Петрович Дня\n" \
        "̲С̲т̲а̲т̲а - статистика по Петровичам\n" \
        "...? -  вернёт да или нет. \n" \
        "̲Р̲а̲н̲д̲о̲м N[,M] (N,M - от и до) - рандомное число в заданном диапазоне\n" \
        "̲П̲о̲г̲о̲д̲а [N] (N - название города(Самара, Питер, Сызрань, Прибой)) - погода в городе\n" \
        "̲О̲б̲о̲с̲р̲а̲т̲ь [N] - рандомное оскорбление. N - что/кто либо\n" \
        "̲П̲о̲х̲в̲а̲л̲и̲т̲ь [N] - рандомная похвала. N - что/кто либо\n" \
        "̲Ц̲и̲т̲а̲т̲а + пересылаемое сообщение - сохраняет в цитатник сообщение(я)\n" \
        "̲Ц̲и̲т̲а̲т̲ы [N[,M]]- просмотр сохранённых цитат. Возможные комбинации - N - номер страницы, N - фраза для поиска, N - фраза для поиска, M - номер страницы\n" \
        "̲К̲л̲а̲в̲а/̲с̲к̲р̲ы̲т̲ь - показывает/убирает клавиатуру\n" \
        "̲П̲о̲м̲о̲щ̲ь - помощь\n" \
        "̲Г̲и̲т - ссылка на гит \n" \
        "̲Ф̲и̲ч̲а - добавляет фичу в список \n" \
        "̲Ф̲и̲ч̲и - вывод всех актуальных фич \n" \
        "̲А̲н̲е̲к̲д̲о̲т [N] - присылает случайный анекдот. N=[1-Анекдот, 2-Рассказы, 3-Стишки, 4-Афоризмы, 5-Цитаты, 6-Тосты, 8-Статусы. Добавляем 10, тогда будет (+18)] \n"

    student_help = \
        "\n-- команды для группы 6221 --\n" \
        "̲Р̲а̲с̲п̲и̲с̲а̲н̲и̲е - картинка с расписанием\n" \
        "̲У̲ч̲е̲б̲н̲о̲е - ссылка на папку с учебным материалом\n" \
        "̲Л̲е̲к̲ц̲и̲и - ссылка на папку с моими лекциями\n" \
        "̲Н̲е̲д̲е̲л̲я - номер текущей учебной недели\n" \
        "̲П̲о̲ч̲т̲а - почты преподов\n"

    admin_help = \
        "\n--для администраторов--\n" \
        "̲У̲п̲р̲а̲в̲л̲е̲н̲и̲е (N,M) - N - chat_id, M - сообщение\n" \
        "̲С̲т̲р̲и̲м [N] (N - ссылка на стрим) \n" \
        "̲С̲т̲а̲р̲т/̲С̲т̲о̲п [N]- возобновляет/продолжает работу Петровича. С параметром можно отключить нужный модуль (синички)\n" \
        "̲Б̲а̲н/̲Р̲а̲з̲б̲а̲н N - N - пользователь \n"

    help_text += default_help
    if is_student:
        help_text += student_help
    if is_admin:
        help_text += admin_help

    return help_text


def get_bad_words():
    return ['еба', 'ебa', 'eба', 'eбa', 'ёба', 'ёбa', 'пидор', 'пидoр', 'пидоp', 'пидop', 'пидар', 'пидaр',
            'пидаp', 'пидap', "пидр", "пидp", 'гандон', 'годнон', 'хуй', 'пизд', 'бля', 'шлюха', 'мудак',
            'говно', 'моча', 'залупа', 'гей', 'сука', 'дурак', 'говно', 'жопа', 'ублюдок', 'мудак']


def get_bad_answers():
    return ['как же вы меня затрахали...', 'ты обижаешь бота?', 'тебе заняться нечем?', '...',
            'о боже', 'тебе не стыдно?', 'зачем ты так?', 'что я тебе сделал?', 'чего ты добился?']


def get_sorry_phrases():
    return ["лан", "нет", "окей", "ничего страшного", "Петрович любит тебя", "я подумаю", "ой всё",
            "ну а чё ты :(", "всё хорошо", "каво", "сь", '...', 'оке', 'ладно, но больше так не делай']


def get_teachers_email():
    emails = [
        [
            "Лёзина Ирина Викторовна",
            "chuchyck@yandex.ru"
        ],
        [
            "Лёзин Илья Александрович",
            "ilyozin@mail.ru"
        ],
        [
            "Солдатова Ольга Петровна",
            "op-soldatova@yandex.ru"
        ]
    ]
    result_text = "Почты преподов\n\n"
    for email in emails:
        result_text += "{} - {}\n".format(email[0], email[1])
    return result_text
