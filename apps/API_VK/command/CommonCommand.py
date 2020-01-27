from datetime import datetime

from apps.Statistics.models import Service


class CommonCommand:
    """
    # Имена, на которые откликается команда
        names - Текст в помощи
        help_text - Клавиатура
        keyboard - Команда для ?
        access - Команда для лс
        for_lk - Команда для конф
        for_conversations - Требуются пересылаемые сообщения
        need_fwd - Требуются аргументы(число)
        need_args - Требуются интовые аргументы (позиции)
        check_int_args - Проверить позиционные аргументы на int
        api - Работает ли команда для api
    """

    def __init__(self,
                 names,
                 help_text=None,
                 detail_help_text=None,
                 keyboard=None,
                 access='user',
                 for_lk=False,
                 for_conversations=False,
                 need_fwd=False,
                 need_args=False,
                 check_int_args=None,
                 api=True,
                 ):
        self.names = names
        self.help_text = help_text
        self.detail_help_text = detail_help_text
        self.keyboard = keyboard
        self.access = access
        self.for_lk = for_lk
        self.for_conversations = for_conversations
        self.need_fwd = need_fwd
        self.need_args = need_args
        self.check_int_args = check_int_args
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
        error = f"Команда доступна только для пользователей с уровнем прав {role_translator[role]}"
        raise RuntimeError(error)

    def check_args(self):
        if self.vk_event.args:
            if len(self.vk_event.args) >= self.need_args:
                return True
            else:
                error = "Передано недостаточно аргументов"
                raise RuntimeError(error)

        error = "Для работы команды требуются аргументы"
        raise RuntimeError(error)

    def check_int_arg_range(self, arg, val1, val2, banned_list=None):
        if val1 <= arg <= val2:
            if banned_list:
                if arg not in banned_list:
                    return True
                else:
                    error = f"Аргумент не может принимать значение {arg}"
                    raise RuntimeError(error)
            else:
                return True
        else:
            error = f"Значение может быть в диапазоне [{val1};{val2}]"
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
                raise RuntimeError(error)
        return True

    def check_lk(self):
        if self.vk_event.from_user:
            return True

        error = "Команда работает только в ЛС"
        raise RuntimeError(error)

    def check_fwd(self):
        if self.vk_event.fwd:
            return True

        error = "Перешлите сообщения"
        raise RuntimeError(error)

    def check_conversation(self):
        if self.vk_event.from_chat:
            return True

        error = "Команда работает только в беседах"
        raise RuntimeError(error)

    def check_command_time(self, name, seconds):
        entity, created = Service.objects.get_or_create(name=name)
        if created:
            return True
        update_datetime = entity.update_datetime
        delta_seconds = (datetime.now() - update_datetime).seconds
        if delta_seconds < seconds:
            error = f"Нельзя часто вызывать команды стоп и старта. Осталось {seconds - delta_seconds} секунд"
            raise RuntimeError(error)
        entity.name = name
        entity.save()
        return True

    def check_api(self):
        if self.vk_event.api:
            error = "Команда не доступна для API"
            raise RuntimeError(error)
        return True


role_translator = {
    'admin': "администратор",
    'moderator': "модератор",
    'minecraft': "майнкрафт",
    'terraria': "террария",
    'student': "студент",
}
