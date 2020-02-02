from apps.API_VK.command.CommonCommand import CommonCommand, role_translator
from apps.API_VK.models import VkUser


def get_users(chat_id, who):
    params = {'chats__chat_id': chat_id, f'is_{who}': True}
    return list(VkUser.objects.filter(**params))


def get_roles(user):
    roles = role_translator.keys()
    active_roles = []
    for role in roles:
        role_true = getattr(user, f'is_{role}')
        if role_true:
            active_roles.append(role_translator[role])
    return active_roles


class Who(CommonCommand):
    def __init__(self):
        names = ["кто"]
        help_text = "Кто - присылает список людей с определённой ролью в конфе"
        detail_help_text = "Кто [(N)] - присылает список людей с ролью N в данной конфе. Доступные роли: админ, модератор, студент, майнкрафт, террария, забанен. Если передать аргумент 'я' или не указывать, то выведутся роли пользователя"
        super().__init__(names, help_text, detail_help_text)

    def start(self):
        if self.vk_event.args is None or self.vk_event.args[0] in ["я"]:
            roles = get_roles(self.vk_event.sender)
            if len(roles) > 0:
                result = "\n".join(roles)
                return str(result)
            else:
                return "Нет прав :("
        else:
            self.check_args(1)
            arg = self.vk_event.args[0]
            self.check_conversation()
            if arg in ['moderators', 'moderator', 'moders', 'moder', 'модераторы', 'модератор', 'модеры', 'модер']:
                who = 'moderator'
            elif arg in ['administrations', 'administration', 'администрация', 'админы', 'админ', 'главный', 'власть']:
                who = 'admin'
            elif arg in ['students', 'student', 'студенты', 'студент']:
                who = 'student'
            elif arg in ['minecraft', 'майнкрафт']:
                who = 'minecraft'
            elif arg in ['terraria', 'террария']:
                who = 'terraria'
            elif arg in ['banned', 'ban', 'забанены', 'забанен', 'бан']:
                who = 'banned'
            else:
                return "Не знаю такой роли"
            users = get_users(self.vk_event.chat.chat_id, who)
            if len(users) > 0:
                users_list = [str(user) for user in users]
                result = "\n".join(users_list)
                return str(result)
            else:
                return "Нет людей с данной ролью"
