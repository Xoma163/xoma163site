import datetime

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.models import PetrovichGames, PetrovichUser


class Petrovich(CommonCommand):
    def __init__(self):
        names = ["петрович", "женя"]
        help_text = "̲П̲е̲т̲р̲о̲в̲и̲ч - мини-игра, определяющая кто Петрович Дня"
        super().__init__(names, help_text, for_conversations=True)

    def start(self):
        today = datetime.datetime.now()
        winner_today = PetrovichGames.objects.filter(date__year=today.year,
                                                     date__month=today.month,
                                                     date__day=today.day,
                                                     chat=self.vk_event.chat).last()
        if winner_today is not None:
            if winner_today.user.name in ["Евгений", "Женя"]:
                self.vk_bot.send_message(self.vk_event.chat_id, "Женя дня - %s" % winner_today.user)
            else:
                self.vk_bot.send_message(self.vk_event.chat_id, "Петрович дня - %s" % winner_today.user)
            return

        # order_by ? = random
        winner = PetrovichUser.objects.filter(chat=self.vk_event.chat).order_by("?").first().user
        PetrovichGames.objects.filter(chat=self.vk_event.chat).delete()
        new_winner = PetrovichGames()
        new_winner.user = winner
        new_winner.chat = self.vk_event.chat
        new_winner.save()
        winner_petrovich = PetrovichUser.objects.filter(user=winner, chat=self.vk_event.chat).first()
        winner_petrovich.wins = int(winner_petrovich.wins) + 1
        winner_petrovich.save()
        self.vk_bot.send_message(self.vk_event.chat_id, "Такс такс такс, кто тут у нас")
        who = "Петрович"
        if winner.name in ["Евгений", "Женя"]:
            who = "Женя"
        self.vk_bot.send_message(self.vk_event.chat_id,
                                 "Наш сегодняшний {} дня - [{}|{} {}]".format(who, winner.nickname, winner.name,
                                                                              winner.surname))
