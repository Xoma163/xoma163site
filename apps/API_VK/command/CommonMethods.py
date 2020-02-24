import random
import re

import threading


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


def check_user_group(user, role):
    group = user.groups.filter(name=role)
    return group.exists()


def get_user_groups(user):
    groups = user.groups.all().values()
    return [group['name'] for group in groups]


def _send_messages_thread(vk_bot, users, message):
    for user in users:
        vk_bot.parse_and_send_msgs(user.user_id, message)


def send_messages(vk_bot, users, message):
    thread = threading.Thread(target=_send_messages_thread, args=(vk_bot, users, message,))
    thread.start()
