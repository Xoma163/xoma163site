from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.models import Words


def get_from_db(field_name):
    my_field = {field_name + "__isnull": False, 'type': 'good'}
    try:
        word = getattr(Words.objects.filter(**my_field).order_by('?').first(), field_name).lower()
    except AttributeError:
        word = "Нет такого слова :("
    except Exception as e:
        word = "Нет такого слова :( Ошибочка - {}".format(str(e))
    return word


def add_phrase_before(smth, word, field_name):
    print(field_name)
    if field_name[1] == '1':
        return "{}, ты {}".format(smth, word)
    elif field_name[1] == 'm':
        return "{}, вы {}".format(smth, word)
    else:
        return "EXCEPTION LOLOLOL"


class Praise(CommonCommand):
    def __init__(self):
        names = ["похвалить", "похвали", "хвалить"]
        help_text = "̲П̲о̲х̲в̲а̲л̲и̲т̲ь [N[,M] - рандомная похвала. N - что-то/род и число, M - род и число"
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
                msg = "спс))"
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
