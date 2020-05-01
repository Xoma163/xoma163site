from apps.API_VK.APIs.rzhunemogy_joke import get_joke
from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import get_inline_keyboard


class Joke(CommonCommand):
    def __init__(self):
        names = ["анекдот", "анек", "а", "a"]
        help_text = "Анекдот - присылает случайный анекдот"
        detail_help_text = "Анекдот [N=1] - присылает случайный анекдот. N=;\n" \
                           "1 — Анекдоты\n" \
                           "2 — Рассказы\n" \
                           "3 — Стишки\n" \
                           "4 — Афоризмы\n" \
                           "5 — Цитаты\n" \
                           "6 — Тосты\n" \
                           "8 — Статусы\n" \
                           "11 — Анекдоты (18+)\n" \
                           "12 — Рассказы (18+)\n" \
                           "13 — Стишки (18+)\n" \
                           "14 — Афоризмы (18+)\n" \
                           "15 — Цитаты (18+)\n" \
                           "16 — Тосты (18+)\n" \
                           "18 — Статусы (18+)\n"
        super().__init__(names, help_text, detail_help_text, int_args=[0])

    def start(self):
        if self.vk_event.args is None:
            a_type = 1
        else:
            a_type = self.vk_event.args[0]
            self.check_number_arg_range(a_type, 1, 19, [9, 10, 17, 19])

        msg = get_joke(a_type)
        if self.vk_event.from_api:
            return msg
        else:
            return {"msg": msg, "keyboard": get_inline_keyboard(self.names[0], args={"a_type": a_type})}
