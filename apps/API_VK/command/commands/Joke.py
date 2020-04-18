from apps.API_VK.APIs.rzhunemogy_joke import get_joke
from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import get_inline_keyboard


class Joke(CommonCommand):
    def __init__(self):
        names = ["анекдот", "анек", "а", "a"]
        help_text = "Анекдот - присылает случайный анекдот"
        detail_help_text = "Анекдот ([N]) - присылает случайный анекдот. N=;\n1-Анекдот;\n2-Рассказы;\n3-Стишки;\n4-Афоризмы;\n5-Цитаты;\n6-Тосты;\n8-Статусы.\nДобавляем 10, тогда будет (+18)]"
        super().__init__(names, help_text, detail_help_text, int_args=[0])

    def start(self):
        if self.vk_event.args is None:
            a_type = 1
        else:
            a_type = self.vk_event.args[0]
            self.check_number_arg_range(a_type, 0, 19, [9, 10, 17, 19])

        msg = get_joke(a_type)
        if self.vk_event.from_api:
            return msg
        else:
            return {"msg": msg, "keyboard": get_inline_keyboard(self.names[0], args={"a_type": a_type})}
