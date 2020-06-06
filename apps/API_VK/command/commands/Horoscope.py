from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.commands.Meme import prepare_meme_to_send
from apps.service.models import Horoscope as HoroscopeModel

zodiac_signs = {
    "овен": 0,
    "телец": 1,
    "близнецы": 2,
    "рак": 3,
    "лев": 4,
    "дева": 5,
    "весы": 6,
    "скорпион": 7,
    "стрелец": 8,
    "козерог": 9,
    "водолей": 10,
    "рыбы": 11
}


class Horoscope(CommonCommand):
    def __init__(self):
        names = ["гороскоп"]
        help_text = "Гороскоп - мемный гороскоп"
        detail_help_text = "Гороскоп - пришлёт гороскоп на день для каждого знака зодиака\n" \
                           "Гороскоп (знак зодиака) - пришлёт гороскоп для знака зодиака"
        super().__init__(names, help_text, detail_help_text, api=False)

    def start(self):
        if self.vk_event.args:
            try:
                zodiac_sign = self.vk_event.args[0].lower()
                zodiac_index = zodiac_signs[zodiac_sign]
            except KeyError:
                return "Не знаю такого знака зодиака"

            horoscope = HoroscopeModel.objects.first()
            meme = horoscope.memes.all()[zodiac_index]
            prepared_meme = prepare_meme_to_send(self.vk_bot, self.vk_event, meme)
            prepared_meme['msg'] = zodiac_sign.capitalize()
            return prepared_meme

        else:
            horoscope = HoroscopeModel.objects.first()
            for zodiac_sign in zodiac_signs:
                meme = horoscope.memes.all()[zodiac_signs[zodiac_sign]]
                prepared_meme = prepare_meme_to_send(self.vk_bot, self.vk_event, meme)
                prepared_meme['msg'] = zodiac_sign.capitalize()
                self.vk_bot.parse_and_send_msgs_thread(self.vk_event.peer_id, prepared_meme)
