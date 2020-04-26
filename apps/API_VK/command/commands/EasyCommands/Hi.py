from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import random_event


class Hi(CommonCommand):
    def __init__(self):
        names = ["привет", "хай", "даров", "дарова", "здравствуй", "здравствуйте", "привки", "прив", "q", "qq", "ку",
                 "куку", "здаров", "здарова", "хеей", "хало", "hi", "hello"]
        super().__init__(names)

    def start(self):
        return random_event(self.names)
