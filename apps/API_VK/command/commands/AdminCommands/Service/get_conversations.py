from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.models import VkChat


class get_conversations(CommonCommand):
    def __init__(self):
        names = ["get_conversations"]
        help_text = "get_conversations - получить данные о всех беседах"
        super().__init__(names, help_text, access='admin', need_args=1)

    def start(self):
        chats = VkChat.objects.all()
        peer_ids = [chat.chat_id for chat in chats]

        res = self.vk_bot.vk.messages.getConversationsById(
            peer_ids=peer_ids,
            extended=1,
            group_id=self.vk_bot.group_id)
        return res
