from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.Consts import Role


class Control(CommonCommand):
    def __init__(self):
        names = ["отправить", "сообщение"]
        help_text = "Отправить - отправление сообщение в любую конфу"
        detail_help_text = "Отправить (id чата/название чата) (сообщение)"
        super().__init__(names, help_text, detail_help_text, access=Role.ADMIN.name, args=2)

    def start(self):
        try:
            self.int_args = [0]
            self.parse_int()
            msg_chat_id = self.vk_event.args[0]
            chat = self.vk_bot.get_group_id(msg_chat_id)
        except RuntimeError:
            msg_chat_name = self.vk_event.args[0]
            chat = self.vk_bot.get_chat_by_name(msg_chat_name)
        msg = self.vk_event.original_args.split(' ', 1)[1]
        self.vk_bot.send_message(chat.chat_id, msg)
