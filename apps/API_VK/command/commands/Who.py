from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.models import VkUser


def get_users(chat_id, who):
    params = {'chats__chat_id': chat_id, f'is_{who}': True}
    return list(VkUser.objects.filter(**params))


class Who(CommonCommand):
    def __init__(self):
        names = ["кто"]
        help_text = "Кто - присылает список людей с определённой ролью в конфе"
        detail_help_text = "Кто (N) - присылает список людей с ролью N в данной конфе. Доступные роли: админ, модератор, студент, майнкрафт, террария, забанен"
        super().__init__(names, help_text, detail_help_text, for_conversations=True, need_args=1)

    def start(self):
        arg = self.vk_event.args[0]
        if arg in ['moderators', 'moderator', 'moders', 'moder', 'модераторы', 'модератор', 'модеры', 'модер']:
            who = 'moderator'
        elif arg in ['administrations', 'administration', 'администрация', 'админы', 'админ']:
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
        # result = ""
        # for moderator in moderators:
