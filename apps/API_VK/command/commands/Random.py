import random

from apps.API_VK.command.CommonCommand import CommonCommand


class Random(CommonCommand):
    def __init__(self):
        names = ["рандом", "ранд"]
        help_text = "̲Р̲а̲н̲д̲о̲м N[,M] (N,M - от и до) - рандомное число в заданном диапазоне"
        super().__init__(names, help_text, check_int_args=[0, 1])

    def start(self):
        if self.vk_event.args:
            if len(self.vk_event.args) == 2:
                int1 = self.vk_event.args[0]
                int2 = self.vk_event.args[1]
            else:
                int1 = 1
                int2 = self.vk_event.args[0]
        else:
            int1 = 0
            int2 = 1

        if int1 > int2:
            int1, int2 = int2, int1

        rand_int = random.randint(int1, int2)
        return str(rand_int)
