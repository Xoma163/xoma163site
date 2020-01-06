import random
import re


def get_random_item_from_list(my_list, arg=None):
    rand_int = random.randint(0, len(my_list) - 1)
    if arg:
        msg = "{}, ты {}".format(arg, my_list[rand_int].lower())
    else:
        msg = my_list[rand_int]
    return msg


# Вероятность события в процентах
def random_probability(probability):
    rand_int = random.randint(1, 100)
    if rand_int <= probability:
        return True
    else:
        return False


def has_cyrillic(text):
    return bool(re.search('[а-яА-Я]', text))


#
# def wrap_msg(msg_str):
#     return [{'msg': msg_str}]
#
#
# def append_msgs(*msgs):
#     new_msgs = []
#     for msg in msgs:
#         new_msgs += msg
#     return new_msgs
