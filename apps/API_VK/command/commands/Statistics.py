from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.models import PetrovichUser
from apps.games.models import Gamer


class Statistics(CommonCommand):
    def __init__(self):
        names = ["стата", "статистика"]
        help_text = "̲С̲т̲а̲т̲а - статистика по Петровичам"
        super().__init__(names, help_text, for_conversations=True)

    def start(self):
        players = PetrovichUser.objects.filter(chat=self.vk_event.chat).order_by('-wins')
        result_list = []
        for player in players:
            result_list.append([player, player.wins])

        msg = "Наши любимые Петровичи:\n"
        for result in result_list:
            msg += "%s - %s\n" % (result[0], result[1])

        gamers = Gamer.objects.all().order_by('-points')
        result_list = []
        for gamer in gamers:
            result_list.append([gamer, gamer.points])

        msg += "\nПобедители ставок:\n"
        for result in result_list:
            msg += "%s - %s\n" % (result[0], result[1])

        self.vk_bot.send_message(self.vk_event.chat_id, msg)
