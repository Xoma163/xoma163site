import random
import re


def get_random_item_from_list(my_list, arg=None):
    rand_int = random.randint(0, len(my_list) - 1)
    if arg:
        msg = f"{arg}, ты {my_list[rand_int].lower()}"
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


def check_user_role(user, role):
    group = user.groups.filter(name=role)
    return group.exists()
