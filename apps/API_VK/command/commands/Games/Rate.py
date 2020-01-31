from threading import Lock

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import get_random_item_from_list
from apps.API_VK.command.commands.Games.Rates import MIN_GAMERS
from apps.games.models import Gamer  # , RateDelete
from apps.games.models import Rate as RateModel

lock = Lock()


class Rate(CommonCommand):
    def __init__(self):
        names = ["ставка"]
        help_text = "Ставка - делает ставку"
        detail_help_text = "Ставка ([N]) - делает ставку. N - ставка. Без параметра - случайная"
        super().__init__(names, help_text, detail_help_text, check_int_args=[0], for_conversations=True)

    def start(self):
        with lock:

            rates_gamers = RateModel.objects.filter(chat=self.vk_event.chat)
            existed_rate = rates_gamers.filter(user=self.vk_event.sender)

            rate_gamer_str = ""
            for rate_gamer in rates_gamers:
                if rate_gamer.random:
                    rate_gamer_str += f"{str(rate_gamer.user)} - {rate_gamer.rate} (R)\n"
                else:
                    rate_gamer_str += f"{str(rate_gamer.user)} - {rate_gamer.rate}\n"

            if len(existed_rate) > 0:
                return f"Ставка уже поставлена\n" \
                       f"Игроки {len(rates_gamers)}/{MIN_GAMERS}:\n" \
                       f"{rate_gamer_str}"
            if self.vk_event.args:
                random = False
                arg = self.vk_event.args[0]
                self.check_int_arg_range(arg, 1, 100)
            else:
                random = True
                available_list = [x for x in range(1, 101)]
                rates = RateModel.objects.filter(chat=self.vk_event.chat)
                for rate_entity in rates:
                    available_list.pop(available_list.index(rate_entity.rate))
                if len(available_list) == 0:
                    return "Какая-то жесть, 100 игроков в ставке, я не могу больше придумать чисел, играйте(("
                arg = get_random_item_from_list(available_list)

            existed_another_rate = RateModel.objects.filter(chat=self.vk_event.chat, rate=arg)
            if len(existed_another_rate) > 0:
                return "Эта ставка уже поставлена другим игроком"

            if len(Gamer.objects.filter(user=self.vk_event.sender)) == 0:
                Gamer(**{'user': self.vk_event.sender}).save()

            RateModel(
                **{'user': self.vk_event.sender, 'chat': self.vk_event.chat, 'rate': arg, 'random': random}).save()
            if random:
                rate_gamer_str += f"{self.vk_event.sender} - {arg} (R)\n"
            else:
                rate_gamer_str += f"{self.vk_event.sender} - {arg}\n"

            # RateDelete(**{'chat': self.vk_event.chat, 'message_id': self.vk_event.message_id}).save()
            return f"Игроки {len(rates_gamers) + 1}/{MIN_GAMERS}:\n" \
                   f"{rate_gamer_str}"
