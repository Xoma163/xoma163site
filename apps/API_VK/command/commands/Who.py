from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.Consts import Role
from apps.API_VK.models import VkUser


def get_users(chat, who):
    params = {'chats': chat, 'groups__name': who}
    return list(VkUser.objects.filter(**params))


class Who(CommonCommand):
    def __init__(self):
        names = ["кто"]
        help_text = "Кто - присылает список людей с определённой ролью в конфе"
        detail_help_text = "Кто (N) - присылает список людей с ролью N в данной конфе. \n" \
                           "Доступные роли: админ, админ конфы, доверенный, модератор, студент, майнкрафт, майнкрафт " \
                           "уведомления, террария, забанен. \n" \
                           "Чтобы узнать свои права существует команда /права"
        super().__init__(names, help_text, detail_help_text, conversation=True, args=1, api=False)

    def start(self):
        arg = self.vk_event.original_args.lower()
        if arg in ['администрация', 'администратор', 'админы', 'админ', 'главный', 'власть', 'господин']:
            who = Role.ADMIN.name
        elif arg in ['moderators', 'moderator' 'модераторы', 'модератор', 'модеры', 'модер']:
            who = Role.MODERATOR.name
        elif arg in ['студент']:
            who = Role.TERRARIA.name
        elif arg in ['майнкрафт уведомления', 'майн уведомления']:
            who = Role.MINECRAFT_NOTIFY.name
        elif arg in ['майнкрафт', 'майн']:
            who = Role.MINECRAFT.name
        elif arg in ['террария']:
            who = Role.TERRARIA.name
        elif arg in ['забанен', 'бан']:
            who = Role.BANNED.name
        elif arg in ['доверенный', 'проверенный']:
            who = Role.TRUSTED.name
        elif arg in ['админ конфы', 'админ беседы', 'админ конференции', 'админ чата',
                     'администратор конфы', 'администратор беседы', 'администратор конференции', 'администратор чата']:
            return str(self.vk_event.chat.admin)
        else:
            return "Не знаю такой роли"
        users = get_users(self.vk_event.chat, who)
        if len(users) > 0:
            users_list = [str(user) for user in users]
            result = "\n".join(users_list)
            return str(result)
        else:
            return "Нет людей с данной ролью"
