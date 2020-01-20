from apps.API_VK.command.CommonCommand import CommonCommand
from apps.games.models import Gamer
from apps.games.models import PetrovichUser


class Statistics(CommonCommand):
    def __init__(self):
        names = ["стата", "статистика"]
        help_text = "̲С̲т̲а̲т̲а - статистика по Петровичам"
        super().__init__(names, help_text)

    def start(self):
        args_translator = {'петрович': self.get_petrovich,
                           'ставки': self.get_rates,
                           'крестики': self.get_tic_tac_toe}

        if self.vk_event.args:
            arg = self.vk_event.args[0].lower()

            if arg not in args_translator:
                return "Я не знаю такого блока"
            return args_translator[arg]()
        msg = ""
        for val in args_translator.values():
            msg += f"{val()}\n"
        return msg

    def get_petrovich(self):
        if not self.vk_event.chat:
            return ""
        players = PetrovichUser.objects.filter(chat=self.vk_event.chat).order_by('-wins')
        result_list = []
        for player in players:
            result_list.append([player, player.wins])

        msg = "Наши любимые Петровичи:\n"
        for result in result_list:
            msg += "%s - %s\n" % (result[0], result[1])
        return msg

    @staticmethod
    def get_rates():
        gamers = Gamer.objects.exclude(points=0).order_by('-points')
        result_list = []
        for gamer in gamers:
            result_list.append([gamer, gamer.points])

        msg = "Победители ставок:\n"
        for result in result_list:
            msg += "%s - %s\n" % (result[0], result[1])
        return msg

    @staticmethod
    def get_tic_tac_toe():
        gamers = Gamer.objects.exclude(tic_tac_toe_points=0).order_by('-tic_tac_toe_points')
        result_list = []
        for gamer in gamers:
            result_list.append([gamer, gamer.tic_tac_toe_points])

        msg = "Победители крестиков-ноликов:\n"
        for result in result_list:
            msg += "%s - %s\n" % (result[0], result[1])

        return msg
