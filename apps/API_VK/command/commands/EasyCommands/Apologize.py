import random
import time

from apps.API_VK.command.CommonCommand import CommonCommand, get_random_item_from_list


class Apologize(CommonCommand):
    def __init__(self):
        names = ["извинись", "извиняйся"]

        super().__init__(names)

    def start(self):
        phrases = ["Извини", "Нет", "Сам извинись", "за что?", "КАВО", "Ты уверен?"]
        phrase = get_random_item_from_list(phrases)

        self.vk_bot.send_message(self.vk_event.chat_id, phrase)
        if phrase == "Извини":
            rand_int = random.randint(0, 100)
            if rand_int <= 25:
                time.sleep(3)
                self.vk_bot.send_message(self.vk_event.chat_id, "сь")
