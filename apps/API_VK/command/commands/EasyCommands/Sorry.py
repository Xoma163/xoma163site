from apps.API_VK.command.CommonCommand import CommonCommand, get_random_item_from_list
from apps.API_VK.static_texts import get_sorry_phrases


class Sorry(CommonCommand):
    def __init__(self):
        names = ['сори', 'прости', 'извини', 'простите', 'извините', 'извиняюсь']
        super().__init__(names)

    def start(self):
        phrases = get_sorry_phrases()
        msg = get_random_item_from_list(phrases)
        self.vk_bot.send_message(self.vk_event.chat_id, msg)
