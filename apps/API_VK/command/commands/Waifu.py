import random

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import get_inline_keyboard


class Waifu(CommonCommand):
    def __init__(self):
        names = ["вайфу"]
        help_text = "Вайфу - присылает несуществующую вайфу"
        detail_help_text = "Вайфу - присылает несуществующую вайфу\n" \
                           "Вайфу ([{номер}]) - присылает несуществующую вайфу по номеру (0-100000)"
        super().__init__(names, help_text, detail_help_text, int_args=[0])

    def start(self):
        WAIFUS_COUNT = 100000
        if self.vk_event.args:
            waifu_number = self.vk_event.args[0]
            self.check_number_arg_range(waifu_number, 0, WAIFUS_COUNT)
        else:
            waifu_number = random.randint(0, WAIFUS_COUNT)
        URL = f"https://www.thiswaifudoesnotexist.net/example-{waifu_number}.jpg"
        attachment = self.vk_bot.upload_photo(URL)

        if self.vk_event.args:
            keyboard = get_inline_keyboard(self.names[0], "Следующая", args={"waifu_number": waifu_number + 1})
        else:
            keyboard = get_inline_keyboard(self.names[0])
        return {"msg": waifu_number, "attachments": [attachment], "keyboard": keyboard}
