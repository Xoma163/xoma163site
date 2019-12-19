from apps.API_VK.command.CommonCommand import CommonCommand


class Hi(CommonCommand):
    def __init__(self):
        names = ["привет", "хай", "даров", "дарова", "здравствуй", "здравствуйте", "привки", "прив", "q", "qq", "ку",
                 "куку", "здаров", "здарова"]
        super().__init__(names)

    def start(self):
        return "Хай"
