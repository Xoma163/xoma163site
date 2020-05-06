from apps.API_VK.command import Role
from apps.API_VK.command.CommonCommand import CommonCommand


class update_users(CommonCommand):
    def __init__(self):
        names = ["update_users"]
        help_text = "update_users - обновляет данные о пользователях в БД"
        super().__init__(names, help_text, access=Role.ADMIN.name)

    def start(self):
        self.vk_bot.update_users()
        return 'done'
