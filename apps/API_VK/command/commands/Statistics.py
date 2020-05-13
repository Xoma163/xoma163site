from apps.API_VK.command.CommonCommand import CommonCommand
from apps.games.models import Gamer
from apps.games.models import PetrovichUser


class Statistics(CommonCommand):
    def __init__(self):
        names = ["стата", "статистика"]
        help_text = "Стата - статистика по победителям игр"
        detail_help_text = "Стата [модуль=все] - статистика. Модули:\n" \
                           "петрович, ставки, крестики, рулетка, коднеймс"
        super().__init__(names, help_text, detail_help_text, conversation=True)

    def start(self):
        args_translator = {'петрович': self.get_petrovich,
                           'ставки': self.get_rates,
                           'крестики': self.get_tic_tac_toe,
                           'коднеймс': self.get_codenames,
                           'рулетка': self.get_roulettes,
                           }

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
        players = PetrovichUser.objects \
            .filter(chat=self.vk_event.chat) \
            .filter(user__chats=self.vk_event.chat) \
            .order_by('-wins')
        result_list = []
        for player in players:
            result_list.append([player, player.wins])

        msg = "Наши любимые Петровичи:\n"
        for result in result_list:
            msg += "%s - %s\n" % (result[0], result[1])
        return msg

    def get_rates(self):
        gamers = Gamer.objects.filter(user__chats=self.vk_event.chat).exclude(points=0).order_by('-points')
        result_list = []
        for gamer in gamers:
            result_list.append([gamer, gamer.points])

        msg = "Победители ставок:\n"
        for result in result_list:
            msg += "%s - %s\n" % (result[0], result[1])
        return msg

    def get_tic_tac_toe(self):
        gamers = Gamer.objects.filter(user__chats=self.vk_event.chat).exclude(tic_tac_toe_points=0).order_by(
            '-tic_tac_toe_points')
        result_list = []
        for gamer in gamers:
            result_list.append([gamer, gamer.tic_tac_toe_points])

        msg = "Победители крестиков-ноликов:\n"
        for result in result_list:
            msg += "%s - %s\n" % (result[0], result[1])

        return msg

    def get_codenames(self):
        gamers = Gamer.objects.filter(user__chats=self.vk_event.chat).exclude(codenames_points=0).order_by(
            '-codenames_points')
        result_list = []
        for gamer in gamers:
            result_list.append([gamer, gamer.codenames_points])

        msg = "Победители коднеймса:\n"
        for result in result_list:
            msg += "%s - %s\n" % (result[0], result[1])

        return msg

    def get_roulettes(self):
        gamers = Gamer.objects.filter(user__chats=self.vk_event.chat).exclude(roulette_points=0).order_by(
            '-roulette_points')
        result_list = []
        for gamer in gamers:
            result_list.append([gamer, gamer.roulette_points])

        msg = "Очки рулетки:\n"
        for result in result_list:
            msg += "%s - %s\n" % (result[0], result[1])

        return msg
