from apps.API_VK.command.CommonCommand import CommonCommand, get_random_item_from_list
from apps.API_VK.models import Words
from apps.API_VK.static_texts import get_bad_answers


def get_from_db(field_name):
    my_field = {field_name + "__isnull": False, 'type': 'bad'}
    try:
        word = getattr(Words.objects.filter(**my_field).order_by('?').first(), field_name).lower()
    except AttributeError:
        word = "Нет такого слова :("
    except Exception as e:
        word = "Нет такого слова :( Ошибочка - {}".format(str(e))
    return word


def add_phrase_before(smth, word, field_name):
    if field_name[1] == '1':
        return "{}, ты {}".format(smth, word)
    elif field_name[1] == 'm':
        return "{}, вы {}".format(smth, word)
    else:
        return "EXCEPTION LOLOLOL"


class Scold(CommonCommand):
    def __init__(self):
        names = ["обосрать", "обосри"]
        help_text = "̲О̲б̲о̲с̲р̲а̲т̲ь [N[,M]] - рандомное оскорбление. N - что-то/род и число, M - род и число"
        super().__init__(names, help_text)

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

        if self.vk_event.args:
            args = self.vk_event.args
            if args[0].lower() == "петрович":
                msg = get_random_item_from_list(get_bad_answers())
            elif args[0].lower() in translator:
                msg = get_from_db(translator[args[0].lower()])
            else:
                msg = add_phrase_before(args[0], get_from_db(translator['м1']), translator['м1'])
            if len(self.vk_event.args) >= 2:

                if args[0].lower() not in translator and args[1].lower() not in translator:
                    msg = "Неверный аргумент определения пола и числа. Доступные: {}".format(
                        str(list(translator.keys())))
                else:
                    if args[1].lower() in translator:
                        args[0], args[1] = args[1], args[0]
                    msg = add_phrase_before(args[1], get_from_db(translator[args[0].lower()]),
                                            translator[args[0].lower()])
        else:
            msg = get_from_db(translator['м1'])

        self.vk_bot.send_message(self.vk_event.chat_id, msg)

        # if self.vk_event.args:
        #     if self.vk_event.args[0].lower() == "петрович":
        #         msg = get_random_item_from_list(get_bad_answers())
        #     else:
        #         msg = get_random_item_from_list(get_insults(), self.vk_event.args[0])
        # else:
        #     msg = get_random_item_from_list(get_insults())
        # self.vk_bot.send_message(self.vk_event.chat_id, msg)
