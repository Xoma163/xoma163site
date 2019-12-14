from apps.API_VK.command.CommonCommand import CommonCommand, check_int_arg_range
from apps.games.models import Gamer
# from apps.games.games.Rate.Rate import start as start_game
from apps.games.models import Rate as RateModel


class Rate(CommonCommand):
    def __init__(self):
        names = ["ставка"]
        super().__init__(names, check_args=1, check_int_args=[0], for_conversations=True)

    def start(self):
        rate = self.vk_event.args[0]

        if not check_int_arg_range(self.vk_bot, self.vk_event, rate, 0, 1):
            return

        existed_rate = RateModel.objects.filter(chat=self.vk_event.chat, user=self.vk_event.sender)
        if len(existed_rate) > 0:
            self.vk_bot.send_message(self.vk_event.chat_id, "Ставка уже поставлена")
            return

        gamer = Gamer.objects.filter(user=self.vk_event.sender)
        if len(gamer) == 0:
            gamer = Gamer()
            gamer.user = self.vk_event.sender
            gamer.save()

        rate = RateModel()
        rate.user = self.vk_event.sender
        rate.chat = self.vk_event.chat
        rate.rate = rate
        rate.save()
        self.vk_bot.send_message(self.vk_event.chat_id, "Ставка принята")
        #
        # start_game(self.vk_event.sender, arg)
        # pass
