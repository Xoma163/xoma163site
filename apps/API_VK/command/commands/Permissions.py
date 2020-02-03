from apps.API_VK.command.CommonCommand import CommonCommand, role_translator


def get_roles(user):
    roles = role_translator.keys()
    active_roles = []
    for role in roles:
        role_true = getattr(user, f'is_{role}')
        if role_true:
            active_roles.append(role_translator[role])
    return active_roles


class Permissions(CommonCommand):
    def __init__(self):
        names = ["права"]
        help_text = "Права - присылает список ваших прав"
        super().__init__(names, help_text)

    def start(self):

        if self.vk_event.args:
            try:
                user = self.vk_bot.get_user_by_name(self.vk_event.args, self.vk_event.chat)
            except RuntimeError as e:
                return str(e)
        else:
            user = self.vk_event.sender

        roles = get_roles(user)
        if len(roles) > 0:
            result = "\n".join(roles)
            return str(result)
        else:
            return "Нет прав :("
