import random

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.games.models import Gamer
from apps.games.models import Rate as RateModel


class Rate(CommonCommand):
    def __init__(self):
        names = ["ставка"]
        super().__init__(names, check_int_args=[0], for_conversations=True)

    def start(self):
        if self.vk_event.args:
            arg = self.vk_event.args[0]
            if not self.check_int_arg_range(arg, 1, 100):
                return
        else:
            arg = random.randint(1, 100)

        existed_rate = RateModel.objects.filter(chat=self.vk_event.chat, user=self.vk_event.sender)
        if len(existed_rate) > 0:
            self.vk_bot.send_message(self.vk_event.chat_id, "Ставка уже поставлена")
            return

        existed_another_rate = RateModel.objects.filter(chat=self.vk_event.chat, rate=arg)
        if len(existed_another_rate) > 0:
            self.vk_bot.send_message(self.vk_event.chat_id, "Эта ставка уже поставлена другим игроком")
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

        self.vk_bot.send_message(self.vk_event.chat_id, "Ставка принята - {}".format(arg))
        #
        # start_game(self.vk_event.sender, arg)
        # pass
