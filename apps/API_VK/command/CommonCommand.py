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


# def check_sender_banned(vk_bot, vk_event):
#     if not vk_event.sender.is_banned:
#         return True
#     # vk_bot.send_message(vk_event.chat_id, "У вас бан")
#     return False


def check_sender_minecraft(vk_bot, vk_event):
    if vk_event.sender.is_minecraft:
        return True
    vk_bot.send_message(vk_event.chat_id, "Команда доступна только майнкрафтерам")
    return False


# ToDo: проверка на количество введёных аргументов
def check_args(vk_bot, vk_event, size=None):
    if vk_event.args:
        return True

    vk_bot.send_message(vk_event.chat_id, "Для работы команды требуются аргументы")
    return False


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


class CommonCommand:

    def __init__(self, names, help_text=None, for_admin=False, for_moderator=False, for_student=False, for_lk=False,
                 for_conversations=False, check_fwd=False, check_args=False):
        self.names = names
        self.help_text = help_text
        self.for_admin = for_admin
        self.for_moderator = for_moderator
        self.for_student = for_student
        self.for_lk = for_lk
        self.for_conversations = for_conversations
        self.check_fwd = check_fwd
        self.check_args = check_args

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

    def start(self):
        return True

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
            if not check_args(self.vk_bot, self.vk_event):
                raise RuntimeError("Для работы команды требуются аргументы")
