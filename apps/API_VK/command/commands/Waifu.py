import random

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import get_inline_keyboard


class Waifu(CommonCommand):
    def __init__(self):
        names = ["вайфу"]
        help_text = "Вайфу - присылает несуществующую вайфу"
        super().__init__(names, help_text)

    def start(self):
        WAIFUS_COUNT = 100000

        random_waifu_number = random.randint(0, WAIFUS_COUNT)
        URL = f"https://www.thiswaifudoesnotexist.net/example-{random_waifu_number}.jpg"
        attachment = self.vk_bot.upload_photo(URL)
        return {"attachments": [attachment], "keyboard": get_inline_keyboard(self.names[0])}
