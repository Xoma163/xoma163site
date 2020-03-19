from apps.API_VK.command.CommonCommand import CommonCommand

class Control(CommonCommand):
    def __init__(self):
        names = ["управление", "сообщение"]
        help_text = "Управление - отправление сообщение в любую конфу"
        detail_help_text = "Управление (N,M) - N - chat_id, M - сообщение"
        super().__init__(names, help_text, detail_help_text, access='admin', args=2, int_args=[0])

    def start(self):
        msg_chat_id = self.vk_event.args[0]
        msg = self.vk_event.params_without_keys.split(' ', 1)[1]

        self.vk_bot.send_message(self.vk_bot.get_group_id(msg_chat_id), msg)
