from datetime import datetime

from apps.Statistics.models import Service


class CommonCommand:

    def __init__(self, names,
                 help_text=None,
                 keyboard=None,
                 access='user',
                 for_lk=False,
                 for_conversations=False,
                 need_fwd=False,
                 need_args=False,
                 check_int_args=None,
                 api=True,
                 ):
        # Имена, на которые откликается команда
        self.names = names
        # Текст в помощи
        self.help_text = help_text
        # Клавиатура
        self.keyboard = keyboard
        # Команда для ?
        self.access = access
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

        # Работает ли команда для api
        self.api = api

        self.vk_bot = None
        self.vk_event = None

    def accept(self, vk_event):
        if vk_event.command in self.names:
            return True

        return False

    def check_and_start(self, vk_bot, vk_event):
        self.vk_bot = vk_bot
        self.vk_event = vk_event

        self.checks()
        return self.start()

    def checks(self):
        if not self.api:
            self.check_api()

        if self.access != 'user':
            self.check_sender(self.access)

        if self.for_lk:
            self.check_lk()
        if self.for_conversations:
            self.check_conversation()
        if self.need_fwd:
            self.check_fwd()
        if self.need_args:
            self.check_args()
        if self.check_int_args:
            self.parse_int_args()

    def start(self):
        pass

    # HELPERS:

    def check_sender(self, role):
        if getattr(self.vk_event.sender, 'is_' + role):
            return True
        error = "Команда доступна только для пользователей с уровнем прав {}".format(role_translator[role])
        # self.vk_bot.send_message(self.vk_event.peer_id, error)
        raise RuntimeError(error)

    def check_args(self):
        if self.vk_event.args:
            if len(self.vk_event.args) >= self.need_args:
                return True
            else:
                error = "Передано недостаточно аргументов"
                # self.vk_bot.send_message(self.vk_event.peer_id, error)
                raise RuntimeError(error)

        error = "Для работы команды требуются аргументы"
        # self.vk_bot.send_message(self.vk_event.peer_id, error)
        raise RuntimeError(error)

    def check_int_arg_range(self, arg, val1, val2, banned_list=None):
        if val1 <= arg <= val2:
            if banned_list:
                if arg not in banned_list:
                    return True
                else:
                    error = "Аргумент не может принимать это значение".format(val1, val2)
                    # self.vk_bot.send_message(self.vk_event.peer_id, error)
                    raise RuntimeError(error)
            else:
                return True
        else:
            error = "Значение может быть в диапазоне [{};{}]".format(val1, val2)
            # self.vk_bot.send_message(self.vk_event.peer_id, error)
            raise RuntimeError(error)

    def parse_int_args(self):
        if not self.vk_event.args:
            return True
        for checked_arg_index in self.check_int_args:
            try:
                if len(self.vk_event.args) - 1 >= checked_arg_index:
                    self.vk_event.args[checked_arg_index] = int(self.vk_event.args[checked_arg_index])
            except ValueError:
                error = "Аргумент должен быть целочисленным"
                # self.vk_bot.send_message(self.vk_event.peer_id, error)
                raise RuntimeError(error)
        return True

    def check_lk(self):
        if self.vk_event.from_user:
            return True

        error = "Команда работает только в ЛС"
        # self.vk_bot.send_message(self.vk_event.peer_id, error)
        raise RuntimeError(error)

    def check_fwd(self):
        if self.vk_event.fwd:
            return True

        error = "Перешлите сообщения"
        # self.vk_bot.send_message(self.vk_event.peer_id, error)
        raise RuntimeError(error)

    def check_conversation(self):
        if self.vk_event.from_chat:
            return True

        error = "Команда работает только в беседах"
        # self.vk_bot.send_message(self.vk_event.peer_id, error)
        raise RuntimeError(error)

    def check_command_time(self, name, seconds):
        entity, created = Service.objects.get_or_create(name=name)
        if created:
            return True
        update_datetime = entity.update_datetime
        delta_seconds = (datetime.now() - update_datetime).seconds
        if delta_seconds < seconds:
            error = "Нельзя часто вызывать команды стоп и старта. Осталось {} секунд".format(seconds - delta_seconds)
            # self.vk_bot.send_message(self.vk_event.peer_id, error)
            raise RuntimeError(error)
        entity.name = name
        entity.save()
        return True

    def check_api(self):
        if self.vk_event.api:
            error = "Команда не доступна для API"
            # self.vk_bot.send_message(self.vk_event.peer_id, error)
            raise RuntimeError(error)
        return True


role_translator = {
    'admin': "администратор",
    'moderator': "модератор",
    'minecraft': "майнкрафт",
    'terraria': "террария",
    'student': "студент",
}
