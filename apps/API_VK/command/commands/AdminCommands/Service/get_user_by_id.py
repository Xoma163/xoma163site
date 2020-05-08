from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.Consts import Role


class get_user_by_id(CommonCommand):
    def __init__(self):
        names = ["get_user_by_id"]
        help_text = "get_user_by_id - принудительно регистрирует юзера по id"
        super().__init__(names, help_text, access=Role.ADMIN.name, args=1)

    def start(self):
        self.vk_bot.get_user_by_id(self.vk_event.args[0])
        return 'done'
