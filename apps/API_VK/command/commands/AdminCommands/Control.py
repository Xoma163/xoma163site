from apps.API_VK.command.CommonCommand import CommonCommand


class Control(CommonCommand):
    def __init__(self):
        names = ["управление", "сообщение"]
        help_text = "̲У̲п̲р̲а̲в̲л̲е̲н̲и̲е (N,M) - N - chat_id, M - сообщение"
        super().__init__(names, help_text, for_admin=True, need_args=2, check_int_args=[0])

    def start(self):
        msg_chat_id = self.vk_event.args[0]
        msg = self.vk_event.original_args.split(' ', 1)[1]

        self.vk_bot.send_message(self.vk_bot.get_group_id(msg_chat_id), msg)
