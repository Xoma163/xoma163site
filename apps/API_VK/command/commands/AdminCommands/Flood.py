from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.Consts import Role


class Flood(CommonCommand):
    def __init__(self):
        names = ["флуд"]
        help_text = "Флуд - флудит"
        detail_help_text = "Флуд (N) - флудит N сообщений"
        super().__init__(names, help_text, detail_help_text, access=Role.ADMIN, args=1, int_args=[0], api=False)

    def start(self):
        msg = "ыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыы"
        count = self.vk_event.args[0]
        msgs = [{'msg': msg}] * count
        return msgs
