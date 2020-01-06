from datetime import datetime

from apps.Statistics.models import Service


class CommonCommand:

    def __init__(self, names,
                 help_text=None,
                 keyboard_admin=None,
                 keyboard_moderator=None,
                 keyboard_student=None,
                 keyboard_user=None,
                 for_admin=False,
                 for_moderator=False,
                 for_student=False,
                 for_lk=False,
                 for_conversations=False,
                 need_fwd=False,
                 need_args=False,
                 check_int_args=None
                 ):
        # Имена, на которые откликается команда
        self.names = names
        # Текст в помощи
        self.help_text = help_text
        # Клавиша для админа
        self.keyboard_admin = keyboard_admin
        # Клавиша для модератора
        self.keyboard_moderator = keyboard_moderator
        # Клавиша для студента
        self.keyboard_student = keyboard_student
        # Клавиша для юзера
        self.keyboard_user = keyboard_user
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
        self.need_fwd = need_fwd
        # Требуются аргументы(число)
        self.need_args = need_args
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
        return self.start()

    def checks(self):
        if self.for_admin:
            if not self.check_sender_admin():
                raise RuntimeError("Пользователь не админ")
        if self.for_moderator:
            if not self.check_sender_moderator():
                raise RuntimeError("Пользователь не модератор и не админ")
        if self.for_student:
            if not self.check_sender_student():
                raise RuntimeError("Пользователь не студент")
        if self.for_lk:
            if not self.check_lk():
                raise RuntimeError("Команда работает только в ЛС")
        if self.for_conversations:
            if not self.check_conversation():
                raise RuntimeError("Команда работает только в беседах")
        if self.need_fwd:
            if not self.check_fwd():
                raise RuntimeError("Команда работает только в беседах")
        if self.need_args:
            if not self.check_args():
                raise RuntimeError("Для работы команды требуются аргументы")
        if self.check_int_args:
            if not self.parse_int_args():
                raise RuntimeError("Аргумент должен быть целочисленным")

    def start(self):
        pass

    # HELPERS:

    def check_sender_admin(self):
        if self.vk_event.sender.is_admin:
            return True
        self.vk_bot.send_message(self.vk_event.peer_id, "Команда доступна только администраторам")
        return False

    def check_sender_moderator(self):
        if self.vk_event.sender.is_moderator or self.vk_event.sender.is_admin:
            return True
        self.vk_bot.send_message(self.vk_event.peer_id, "Команда доступна только администраторам и модераторам")
        return False

    def check_sender_student(self):
        if self.vk_event.sender.is_student:
            return True
        self.vk_bot.send_message(self.vk_event.peer_id, "Команда доступна только студентам")
        return False

    def check_sender_minecraft(self):
        if self.vk_event.sender.is_minecraft:
            return True
        self.vk_bot.send_message(self.vk_event.peer_id, "Команда доступна только для игроков майна")
        return False

    def check_sender_terraria(self):
        if self.vk_event.sender.is_terraria:
            return True
        self.vk_bot.send_message(self.vk_event.peer_id, "Команда доступна только для игроков террарии")
        return False

    def check_args(self):
        if self.vk_event.args:
            if len(self.vk_event.args) >= self.need_args:
                return True
            else:
                self.vk_bot.send_message(self.vk_event.peer_id, "Передано недостаточно аргументов")
                return False

        self.vk_bot.send_message(self.vk_event.peer_id, "Для работы команды требуются аргументы")
        return False

    def check_int_arg_range(self, arg, val1, val2, banned_list=None):
        if val1 <= arg <= val2:
            if banned_list:
                if arg not in banned_list:
                    return True
                else:
                    self.vk_bot.send_message(self.vk_event.peer_id,
                                             "Аргумент не может принимать это значение".format(val1, val2))
                    return False
            else:
                return True
        else:
            self.vk_bot.send_message(self.vk_event.peer_id,
                                     "Значение может быть в диапазоне [{};{}]".format(val1, val2))
            return False

    def check_int_arg(self, arg):
        try:
            return int(arg), True
        except ValueError:
            self.vk_bot.send_message(self.vk_event.peer_id, "Аргумент должен быть целочисленным")
            return arg, False

    def parse_int_args(self):
        if not self.vk_event.args:
            return True

        for checked_arg_index in self.check_int_args:
            try:
                if len(self.vk_event.args) - 1 >= checked_arg_index:
                    self.vk_event.args[checked_arg_index] = int(self.vk_event.args[checked_arg_index])
            except ValueError:
                self.vk_bot.send_message(self.vk_event.peer_id, "Аргумент должен быть целочисленным")
                return False

        return True

    def check_lk(self):
        if self.vk_event.from_user:
            return True

        self.vk_bot.send_message(self.vk_event.peer_id, "Команда работает только в ЛС")
        return False

    def check_fwd(self):
        if self.vk_event.fwd:
            return True

        self.vk_bot.send_message(self.vk_event.peer_id, "Перешлите сообщения")
        return False

    def check_conversation(self):
        if self.vk_event.from_chat:
            return True

        self.vk_bot.send_message(self.vk_event.peer_id, "Команда работает только в беседах")
        return False

    def check_command_time(self, name, seconds):
        entity, created = Service.objects.get_or_create(name=name)
        if created:
            return True
        update_datetime = entity.update_datetime
        delta_seconds = (datetime.now() - update_datetime).seconds
        if delta_seconds < seconds:
            self.vk_bot.send_message(self.vk_event.peer_id,
                                     "Нельзя часто вызывать команды остановки и старта. Жди ещё {} секунд"
                                     .format(seconds - delta_seconds))
            return False
        entity.name = name
        entity.save()
        return True
