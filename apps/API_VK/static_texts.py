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


def get_bad_words():
    return ['еба', 'ебa', 'eба', 'eбa', 'ёба', 'ёбa', 'пидор', 'пидoр', 'пидоp', 'пидop', 'пидар', 'пидaр',
            'пидаp', 'пидap', "пидр", "пидp", 'гандон', 'годнон', 'хуй', 'пизд', 'бля', 'шлюха', 'мудак',
            'говно', 'моча', 'залупа', 'гей', 'дурак', 'говно', 'жопа', 'ублюдок', 'мудак',
            'сука', 'сукa', 'сyка', 'сyкa', 'cука', 'cукa', 'cyка', 'cyкa', 'суkа', 'суka', 'сykа', 'сyka', 'cуkа',
            'cуka', 'cykа', 'cyka']


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
