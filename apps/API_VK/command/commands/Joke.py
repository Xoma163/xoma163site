from apps.API_VK.APIs.rzhunemogy_joke import get_joke
from apps.API_VK.command.CommonCommand import CommonCommand


class Joke(CommonCommand):
    def __init__(self):
        names = ["анекдот", "анек", "а", "a"]
        help_text = "̲А̲н̲е̲к̲д̲о̲т [N] - присылает случайный анекдот. N=[1-Анекдот, 2-Рассказы, 3-Стишки, 4-Афоризмы, 5-Цитаты, 6-Тосты, 8-Статусы. Добавляем 10, тогда будет (+18)]"
        super().__init__(names, help_text, check_int_args=[0])

    def start(self):
        if self.vk_event.args is None:
            a_type = 1
        else:
            a_type = self.vk_event.args[0]
            if not self.check_int_arg_range(a_type, 0, 19, [9, 10]):
                return

        joke = get_joke(a_type)
        self.vk_bot.send_message(self.vk_event.chat_id, joke)
