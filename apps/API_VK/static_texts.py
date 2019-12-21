def get_keyboard(is_admin=False, is_moderator=False, is_student=False):
    from apps.API_VK.command import STUDENT_BUTTONS, MODERATOR_BUTTONS, ADMIN_BUTTONS, USER_BUTTONS

    buttons = []

    if is_admin:
        buttons += ADMIN_BUTTONS
    if is_moderator:
        buttons += MODERATOR_BUTTONS
    if is_student:
        buttons += STUDENT_BUTTONS
    buttons += USER_BUTTONS

    keyboard = {
        "one_time": False,
        "buttons": buttons
    }
    return keyboard


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
