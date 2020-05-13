import time

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import random_probability, random_event


class Apologize(CommonCommand):
    def __init__(self):
        names = ["извинись", "извиняйся", "извинитесь"]

        super().__init__(names, api=False)

    def start(self):
        phrases = ["Извини", "Нет", "Сам извинись", "за что?", "КАВО", "Ты уверен?"]
        phrase = random_event(phrases)
        self.vk_bot.send_message(self.vk_event.peer_id, phrase)

        # ToDo: запускать асинхронную таску по отправке сообщения, результат ретёрнить
        if phrase == "Извини":
            if random_probability(25):
                time.sleep(3)
                self.vk_bot.send_message(self.vk_event.peer_id, "сь")
