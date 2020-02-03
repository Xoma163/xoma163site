from apps.API_VK.APIs.rzhunemogy_joke import get_joke
from apps.API_VK.command.CommonCommand import CommonCommand


class Joke(CommonCommand):
    def __init__(self):
        names = ["анекдот", "анек", "а", "a"]
        help_text = "Анекдот - присылает случайный анекдот"
        detail_help_text = "Анекдот ([N]) - присылает случайный анекдот. N=;\n1-Анекдот;\n2-Рассказы;\n3-Стишки;\n4-Афоризмы;\n5-Цитаты;\n6-Тосты;\n8-Статусы.\nДобавляем 10, тогда будет (+18)]"
        super().__init__(names, help_text, detail_help_text, check_int_args=[0])

    def start(self):
        if self.vk_event.args is None:
            a_type = 1
        else:
            a_type = self.vk_event.args[0]
            self.check_int_arg_range(a_type, 0, 19, [9, 10, 17, 19])

        joke = get_joke(a_type)
        return joke
