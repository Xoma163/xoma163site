from threading import Lock

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import get_random_item_from_list
from apps.games.models import Gamer
from apps.games.models import Rate as RateModel

lock = Lock()


class Rate(CommonCommand):
    def __init__(self):
        names = ["ставка"]
        super().__init__(names, check_int_args=[0], for_conversations=True)

    def start(self):
        lock.acquire()

        if self.vk_event.args:
            arg = self.vk_event.args[0]
            if not self.check_int_arg_range(arg, 1, 100):
                lock.release()
                return
        else:
            available_list = [x for x in range(1, 101)]
            print(available_list)
            rates = RateModel.objects.filter(chat=self.vk_event.chat)
            for rate_entity in rates:
                available_list.pop(available_list.index(rate_entity.rate))
            if len(available_list) == 0:
                lock.release()
                return "Какая-то жесть, 100 игроков в ставке, я не могу больше придумать чисел, играйте(("
            arg = get_random_item_from_list(available_list)

        existed_rate = RateModel.objects.filter(chat=self.vk_event.chat, user=self.vk_event.sender)
        if len(existed_rate) > 0:
            lock.release()
            return "Ставка уже поставлена"

        existed_another_rate = RateModel.objects.filter(chat=self.vk_event.chat, rate=arg)
        if len(existed_another_rate) > 0:
            lock.release()
            return "Эта ставка уже поставлена другим игроком"

        if len(Gamer.objects.filter(user=self.vk_event.sender)) == 0:
            Gamer(**{'user': self.vk_event.sender}).save()

        RateModel(**{'user': self.vk_event.sender, 'chat': self.vk_event.chat, 'rate': arg}).save()
        lock.release()
        return "Ставка принята - {}".format(arg)
        #
        # start_game(self.vk_event.sender, arg)
        # pass
