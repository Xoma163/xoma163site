import random
from datetime import datetime

from apps.Statistics.models import Service


def check_sender_admin(vk_bot, vk_event):
    if vk_event.sender.is_admin:
        return True
    if vk_event.chat_id is not None:
        vk_bot.send_message(vk_event.chat_id, "Команда доступна только администраторам")
    return False


def check_sender_moderator(vk_bot, vk_event):
    if vk_event.sender.is_moderator or vk_event.sender.is_admin:
        return True
    vk_bot.send_message(vk_event.chat_id, "Команда доступна только администраторам и модераторам")
    return False


def check_sender_student(vk_bot, vk_event):
    if vk_event.sender.is_student:
        return True
    vk_bot.send_message(vk_event.chat_id, "Команда доступна только студентам")
    return False


def check_sender_minecraft(vk_bot, vk_event):
    if vk_event.sender.is_minecraft:
        return True
    vk_bot.send_message(vk_event.chat_id, "Команда доступна только майнкрафтерам")
    return False


def check_args(vk_bot, vk_event, size=1):
    if vk_event.args:
        if len(vk_event.args) >= size:
            return True
        else:
            vk_bot.send_message(vk_event.chat_id, "Передано недостаточно аргументов")
            return False

    vk_bot.send_message(vk_event.chat_id, "Для работы команды требуются аргументы")
    return False


def check_int_arg_range(vk_bot, vk_event, arg, val1, val2, banned_list=None):
    if val1 <= arg <= val2:
        if banned_list:
            if arg not in banned_list:
                return True
            else:
                vk_bot.send_message(vk_event.chat_id, "Аргумент не может принимать это значение".format(val1, val2))
                return False
        else:
            return True
    else:
        vk_bot.send_message(vk_event.chat_id, "Значение может быть в диапазоне [{};{}]".format(val1, val2))
        return False


def check_int_arg(vk_bot, vk_event, arg):
    try:
        return int(arg), True
    except ValueError:
        vk_bot.send_message(vk_event.chat_id, "Аргумент должен быть целочисленным")
        return arg, False


def parse_int_args(vk_bot, vk_event, checked_args):
    for checked_arg_index in checked_args:
        try:
            if len(vk_event.args) - 1 >= checked_arg_index:
                vk_event.args[checked_arg_index] = int(vk_event.args[checked_arg_index])
        except ValueError:
            vk_bot.send_message(vk_event.chat_id, "Аргумент должен быть целочисленным")
            return False
    return vk_event.args


def check_lk(vk_bot, vk_event):
    if vk_event.is_lk:
        return True

    vk_bot.send_message(vk_event.chat_id, "Команда работает только в ЛС")
    return False


def check_fwd(vk_bot, vk_event):
    if vk_event.fwd:
        return True

    vk_bot.send_message(vk_event.chat_id, "Перешлите сообщения")
    return False


def check_conversation(vk_bot, vk_event):
    if not vk_event.is_lk:
        return True

    vk_bot.send_message(vk_event.chat_id, "Команда работает только в беседах")
    return False


def get_random_item_from_list(list, arg=None):
    rand_int = random.randint(0, len(list) - 1)
    if arg:
        msg = "{}, ты {}".format(arg, list[rand_int].lower())
    else:
        msg = list[rand_int]
    return msg


def check_command_time(vk_bot, vk_event, name, seconds):
    entity, created = Service.objects.get_or_create(name=name)
    if created:
        return True
    update_datetime = entity.update_datetime
    delta_seconds = (datetime.now() - update_datetime).seconds
    if delta_seconds < seconds:
        vk_bot.send_message(vk_event.chat_id, "Нельзя часто вызывать команды остановки и старта. Жди ещё {} секунд"
                            .format(seconds - delta_seconds))
        return False
    entity.name = name
    entity.save()
    return True


# Вероятность события в процентах
def random_probability(probability):
    rand_int = random.randint(1, 100)
    if rand_int <= probability:
        return True
    else:
        return False


class CommonCommand:

    def __init__(self, names,
                 help_text=None,
                 for_admin=False,
                 for_moderator=False,
                 for_student=False,
                 for_lk=False,
                 for_conversations=False,
                 check_fwd=False,
                 check_args=False,
                 check_int_args=None
                 ):
        # Имена, на которые откликается команда
        self.names = names
        # Текст в помощи
        self.help_text = help_text
        # Команда для админов
        self.for_admin = for_admin
        # Команда для модераторов
        self.for_moderator = for_moderator
        # Команда для студентов
        self.for_student = for_student
        # Команда для лс
        self.for_lk = for_lk
        # Команда для конф
        self.for_conversations = for_conversations
        # Требуются пересылаемые сообщения
        self.check_fwd = check_fwd
        # Требуются аргументы(число)
        self.check_args = check_args
        # Требуются интовые аргументы (позиции)
        self.check_int_args = check_int_args

        self.vk_bot = None
        self.vk_event = None

    def accept(self, vk_event):
        if vk_event.command not in self.names:
            return False

        return True

    def check_and_start(self, vk_bot, vk_event):
        self.vk_bot = vk_bot
        self.vk_event = vk_event

        self.checks()
        self.start()

    def checks(self):
        if self.for_admin:
            if not check_sender_admin(self.vk_bot, self.vk_event):
                raise RuntimeError("Пользователь не админ")
        if self.for_moderator:
            if not check_sender_moderator(self.vk_bot, self.vk_event):
                raise RuntimeError("Пользователь не модератор и не админ")
        if self.for_student:
            if not check_sender_student(self.vk_bot, self.vk_event):
                raise RuntimeError("Пользователь не студент")
        if self.for_lk:
            if not check_lk(self.vk_bot, self.vk_event):
                raise RuntimeError("Команда работает только в ЛС")
        if self.for_conversations:
            if not check_conversation(self.vk_bot, self.vk_event):
                raise RuntimeError("Команда работает только в беседах")
        if self.check_fwd:
            if not check_fwd(self.vk_bot, self.vk_event):
                raise RuntimeError("Команда работает только в беседах")
        if self.check_args:
            if not check_args(self.vk_bot, self.vk_event, self.check_args):
                raise RuntimeError("Для работы команды требуются аргументы")
        if self.check_int_args:
            res = parse_int_args(self.vk_bot, self.vk_event, self.check_int_args)
            if not res:
                raise RuntimeError("Аргумент должен быть целочисленным")
            else:
                self.vk_event.args = res

    def start(self):
        return True
