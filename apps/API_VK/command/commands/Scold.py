from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import get_random_item_from_list
from apps.API_VK.models import Words
from apps.API_VK.static_texts import get_bad_answers


def get_from_db(field_name):
    my_field = {field_name + "__isnull": False, 'type': 'bad'}
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


def check_key(keys, translator):
    for key in keys:
        if key in translator:
            return key
    return False


class Scold(CommonCommand):
    def __init__(self):
        names = ["обосрать", "обосри", "поругать", "поругай"]
        help_text = "Обосрать - рандомное оскорбление"
        detail_help_text = "Обосрать ([N]) - рандомное оскорбление. N - что-то/род и число. Род и число указываются через ключи: Мужской -м, Женский -ж, Средний -с. Число: единственное -*1, множественное -*м. Т.е. доступные сочетания ключей могут быть следующими: [-м -ж -с -м1 -ж1 -с1 -мм -жм] "

        super().__init__(names, help_text, detail_help_text)

    def start(self):

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
        if self.vk_event.keys_list:
            key = check_key(self.vk_event.keys_list, translator)
            if key:
                translator_key = key
            else:
                msg = f"Неверные ключи определения пола и числа. Доступные: {str(list(translator.keys()))}"
                return msg
        else:
            if self.vk_event.params_without_keys:
                try:
                    user = self.vk_bot.get_user_by_name([self.vk_event.params_without_keys])
                    if user.gender == '1':
                        translator_key = 'ж1'
                    else:
                        translator_key = 'м1'
                except Exception as e:
                    translator_key = 'м1'
            else:
                translator_key = 'м1'

        if self.vk_event.params_without_keys:
            recipient = self.vk_event.params_without_keys
            if "петрович" in recipient:
                msg = get_random_item_from_list(get_bad_answers())
            else:
                word = get_from_db(translator[translator_key])
                msg = add_phrase_before(recipient, word, translator[translator_key])
        else:
            msg = get_from_db(translator[translator_key])
        return msg
