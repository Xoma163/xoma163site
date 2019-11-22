import random

from apps.API_VK.command.CommonCommand import CommonCommand


class Random(CommonCommand):
    def __init__(self):
        names = ["рандом", "ранд"]
        help_text = "̲Р̲а̲н̲д̲о̲м N[,M] (N,M - от и до) - рандомное число в заданном диапазоне"
        super().__init__(names, help_text)

    def start(self):
        if len(self.vk_event.args) == 2:
            try:
                int1 = int(self.vk_event.args[0])
                int2 = int(self.vk_event.args[1])
            except:
                self.vk_bot.send_message(self.vk_event.chat_id, "Аргументы должны быть целочисленными")
                return
        else:
            int1 = 1
            try:
                int2 = int(self.vk_event.args[0])
            except:
                self.vk_bot.send_message(self.vk_event.chat_id, "Аргументы должны быть целочисленными")
                return

        if int1 > int2:
            int1, int2 = int2, int1

        rand_int = random.randint(int1, int2)
        self.vk_bot.send_message(self.vk_event.chat_id, str(rand_int))
