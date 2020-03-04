from datetime import datetime

from apps.API_VK.command.CommonMethods import check_user_group
from apps.service.models import Service


class CommonCommand:
    """
    # names - Имена, на которые откликается команда
        help_text - Текст в помощи
        keyboard - Клавиатура
        access - Команда для ?
        pm - Команда для лс
        conversation - Команда для конф
        fwd - Требуются пересылаемые сообщения
        args - Требуются аргументы(число)
        int_args - Требуются интовые аргументы (позиции)
        api - Работает ли команда для api
    """

    def __init__(self,
                 names,
                 help_text=None,
                 detail_help_text=None,
                 keyboard=None,
                 access='user',
                 pm=False,
                 conversation=False,
                 fwd=False,
                 args=None,
                 int_args=None,
                 api=True,
                 attachments=False
                 ):
        self.names = names
        self.help_text = help_text
        self.detail_help_text = detail_help_text
        self.keyboard = keyboard
        self.access = access
        self.pm = pm
        self.conversation = conversation
        self.fwd = fwd
        self.args = args
        self.int_args = int_args
        self.api = api
        self.attachments = attachments

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
        # Если команда не для api
        if not self.api:
            self.check_api()
        if self.access != 'user':
            self.check_sender(self.access)
        if self.pm:
            self.check_pm()
        if self.conversation:
            self.check_conversation()
        if self.fwd:
            self.check_fwd()
        if self.args:
            self.check_args()
        if self.int_args:
            self.parse_int_args()
        if self.attachments:
            self.check_attachments()

    def start(self):
        pass

    # HELPERS:

    # def check_sender(self, role):
    #     if getattr(self.vk_event.sender, 'is_' + role):
    #         return True
    #     error = f"Команда доступна только для пользователей с уровнем прав {role_translator[role]}"
    #     raise RuntimeError(error)

    def check_sender(self, role):
        if check_user_group(self.vk_event.sender, role):
            return True
        error = f"Команда доступна только для пользователей с уровнем прав {role_translator[role]}"
        raise RuntimeError(error)

    def check_args(self, args=None):
        if args is None:
            args = self.args
        if self.vk_event.args:
            if len(self.vk_event.args) >= args:
                return True
            else:
                error = "Передано недостаточно аргументов"
                raise RuntimeError(error)

        error = "Для работы команды требуются аргументы"
        raise RuntimeError(error)

    @staticmethod
    def check_int_arg_range(arg, val1, val2, banned_list=None):
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
        for checked_arg_index in self.int_args:
            try:
                if len(self.vk_event.args) - 1 >= checked_arg_index:
                    self.vk_event.args[checked_arg_index] = int(self.vk_event.args[checked_arg_index])
            except ValueError:
                error = "Аргумент должен быть целочисленным"
                raise RuntimeError(error)
        return True

    def check_pm(self):
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
        # Если запрос пришёл через api
        if self.vk_event.api:
            error = "Команда недоступна для API"
            raise RuntimeError(error)
        return True

    def check_attachments(self):
        if self.vk_event.attachments:
            return True

        error = "Пришлите вложения"
        raise RuntimeError(error)


role_translator = {
    'admin': "администратор",
    'moderator': "модератор",
    'minecraft': "майнкрафт",
    'terraria': "террария",
    'student': "студент",
    'minecraft_notify': "уведомления майна",
    'user': 'пользователь',
    'ban': 'забанен'
}
