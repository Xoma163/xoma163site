from apps.API_VK.command.CommonCommand import CommonCommand
from apps.games.models import Gamer
# from apps.games.games.Rate.Rate import start as start_game
from apps.games.models import Rate as RateModel


class Rate(CommonCommand):
    def __init__(self):
        names = ["ставка"]
        super().__init__(names, need_args=1, check_int_args=[0], for_conversations=True)

    def start(self):
        arg = self.vk_event.args[0]

        if not self.check_int_arg_range(arg, 1, 100):
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
        rate.rate = arg
        rate.save()
        self.vk_bot.send_message(self.vk_event.chat_id, "Ставка принята")
        #
        # start_game(self.vk_event.sender, arg)
        # pass
