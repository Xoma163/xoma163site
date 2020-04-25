from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import get_random_item_from_list
from apps.API_VK.models import Words
from apps.API_VK.static_texts import get_bad_answers


def get_from_db(field_name, _type):
    my_field = {field_name + "__isnull": False, 'type': _type}
    try:
        word = getattr(Words.objects.filter(**my_field).order_by('?').first(), field_name).lower()
    except AttributeError:
        word = "Нет такого слова :("
    except Exception as e:
        word = f"Нет такого слова :( Ошибочка - {str(e)}"
    return word


def add_phrase_before(recipient, word, field_name):
    if field_name[1] == '1':
        return f"{recipient}, ты {word}"
    elif field_name[1] == 'm':
        return f"{recipient}, вы {word}"
    else:
        return "EXCEPTION LOLOLOL"


translator = {
    'м': 'm1',
    'ж': 'f1',
    'с': 'n1',
    'м1': 'm1',
    'ж1': 'f1',
    'с1': 'n1',
    'мм': 'mm',
    'жм': 'fm'
}


def get_praise_or_scold(vk_bot, vk_event, _type):
    if vk_event.original_args and vk_event.args[-1] in translator:
        translator_key = vk_event.args[-1]
        del vk_event.args[-1]
    else:
        try:
            user = vk_bot.get_user_by_name(vk_event.original_args, vk_event.chat)
            if user.gender == '1':
                translator_key = 'ж1'
            else:
                translator_key = 'м1'
        except RuntimeError:
            translator_key = 'м1'
    if vk_event.args:
        recipient = " ".join(vk_event.args)

        if "петрович" in recipient.lower():
            if _type == 'bad':
                msg = get_random_item_from_list(get_bad_answers())
            elif _type == 'good':
                msg = "спс))"
            else:
                msg = "wtf"
        else:
            word = get_from_db(translator[translator_key], _type)
            msg = add_phrase_before(recipient, word, translator[translator_key])
    else:
        msg = get_from_db(translator[translator_key], _type)
    return msg


def get_praise_or_scold_self(vk_event, _type):
    recipient = vk_event.sender
    if recipient.gender == '1':
        translator_key = 'ж1'
    else:
        translator_key = 'м1'

    word = get_from_db(translator[translator_key], _type)
    msg = add_phrase_before(recipient.name, word, translator[translator_key])
    return msg


class Praise(CommonCommand):
    def __init__(self):
        names = ["похвалить", "похвали", "хвалить"]
        help_text = "Похвалить - рандомная похвала"
        detail_help_text = "Похвалить [кто-то] [род+число] - рандомная похвала\n" \
                           "Род и число указываются через последний аргумент: Мужской м, Женский ж, Средний с. Число: единственное *1, множественное *м\n" \
                           "Т.е. доступные сочетания аргументов могут быть следующими: [м ж с м1 ж1 с1 мм жм]\n" \
                           "Если в качестве параметра передаётся имя, фамилия, логин/id, никнейм, то род выберится из БД\n" \
                           "Пример. /похвалить бабушка ж"
        super().__init__(names, help_text, detail_help_text)

    def start(self):
        return get_praise_or_scold(self.vk_bot, self.vk_event, 'good')
