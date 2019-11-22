from apps.API_VK.command.CommonCommand import CommonCommand


class Control(CommonCommand):
    def __init__(self):
        names = ["управление", "сообщение"]
        super().__init__(names, for_admin=True, check_args=True)

    def start(self):
        # ToDo: вынос в check_args
        if len(self.vk_event.args) < 2:
            self.vk_bot.send_message(self.vk_event.chat_id, "Аргументов должно быть 2")
            return
        msg_chat_id = int(self.vk_event.args[0])
        msg = self.vk_event.original_args.split(' ', 1)[1]

        self.vk_bot.send_message(self.vk_bot.get_group_id(msg_chat_id), msg)
