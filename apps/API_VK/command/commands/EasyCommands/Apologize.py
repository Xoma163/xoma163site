import time

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import get_random_item_from_list, random_probability


class Apologize(CommonCommand):
    def __init__(self):
        names = ["извинись", "извиняйся", "извинитесь"]

        super().__init__(names)

    def start(self):
        # ToDo: Что-то с этим сделать надо

        phrases = ["Извини", "Нет", "Сам извинись", "за что?", "КАВО", "Ты уверен?"]
        phrase = get_random_item_from_list(phrases)
        self.vk_bot.send_message(self.vk_event.chat_id, )

        if phrase == "Извини":
            if random_probability(25):
                time.sleep(3)
                self.vk_bot.send_message(self.vk_event.chat_id, "сь")
