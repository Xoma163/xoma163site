from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import get_random_int


class Random(CommonCommand):
    def __init__(self):
        names = ["рандом", "ранд", 'р', 'p']
        help_text = "Рандом - рандомное число в заданном диапазоне"
        detail_help_text = "Рандом - рандомное число в диапазоне[0:1]\n" \
                           "Рандом N - рандомное число в заданном диапазоне[1:N]\n" \
                           "Рандом N,M - рандомное число в заданном диапазоне[N:M]\n"
        super().__init__(names, help_text, detail_help_text, int_args=[0, 1])

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

        rand_int = get_random_int(int1, int2)
        return str(rand_int)
