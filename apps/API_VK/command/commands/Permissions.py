from apps.API_VK.command import Role
from apps.API_VK.command.CommonCommand import CommonCommand


def get_roles(user):
    active_roles = []
    for group in user.groups.all():
        active_roles.append(Role[group.name].value)
    return active_roles


class Permissions(CommonCommand):
    def __init__(self):
        names = ["права"]
        help_text = "Права - присылает список ваших прав"
        detail_help_text = "Права - присылает ваши права\n" \
                           "Права [N] - права пользователя в беседе. N - имя, фамилия, логин/id, никнейм"

        super().__init__(names, help_text, detail_help_text)

    def start(self):

        if self.vk_event.args:
            self.check_conversation()
            try:
                user = self.vk_bot.get_user_by_name(self.vk_event.args, self.vk_event.chat)
            except RuntimeError as e:
                return str(e)
        else:
            user = self.vk_event.sender

        roles = get_roles(user)
        if len(roles) > 0:
            result = "\n".join(roles)

            if self.vk_event.chat and self.vk_event.chat.admin == user:
                result += "\n" \
                          "админ конфы"
            return result
        else:
            return "Нет прав :("
