from apps.API_VK.command.CommonCommand import CommonCommand


class get_conversations(CommonCommand):
    def __init__(self):
        names = ["get_conversations"]
        help_text = "get_conversations - получить данные о всех беседах"
        super().__init__(names, help_text, for_admin=True, check_args=1)

    def start(self):
        res = self.vk_bot.vk.messages.getConversationsById(
            peer_ids=[2000000001, 2000000003], extended=1, group_id=186416119)
        self.vk_bot.send_message(self.vk_event.chat_id, res)
