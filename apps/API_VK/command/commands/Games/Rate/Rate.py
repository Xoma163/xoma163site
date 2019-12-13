from apps.API_VK.command.CommonCommand import CommonCommand
from apps.games.models import Gamer
# from apps.games.games.Rate.Rate import start as start_game
from apps.games.models import Rate as RateModel


class Rate(CommonCommand):
    def __init__(self):
        names = ["ставка"]
        super().__init__(names, check_args=True, for_conversations=True)

    def start(self):
        arg = self.vk_event.args[0]
        try:
            arg = int(arg)
        except Exception as e:
            self.vk_bot.send_message(self.vk_event.chat_id, "Аргумент должен быть целочисленным")
            return

        if arg < 1 or arg > 100:
            self.vk_bot.send_message(self.vk_event.chat_id, "Аргументы должны быть в диапазоне [1;100]")
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
