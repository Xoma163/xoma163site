from django.db.models import Count

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.models import VkUser
from apps.games.models import Gamer
from apps.games.models import PetrovichUser
from apps.service.models import Meme


class Statistics(CommonCommand):
    def __init__(self):
        names = ["стата", "статистика"]
        help_text = "Стата - статистика по победителям игр или по кол-ву созданных мемов"
        detail_help_text = "Стата [модуль=все] - статистика по победителям игр или по кол-ву созданных мемов. Модули:\n" \
                           "петрович, ставки, крестики, рулетка, коднеймс, мемы"
        super().__init__(names, help_text, detail_help_text, conversation=True)

    def start(self):
        args_translator = {
            'петрович': self.get_petrovich,
            'ставки': self.get_rates,
            'крестики': self.get_tic_tac_toe,
            'коднеймс': self.get_codenames,
            'рулетка': self.get_roulettes,
            'мемы': self.get_memes
        }

        if self.vk_event.args:
            arg = self.vk_event.args[0].lower()

            if arg not in args_translator:
                return "Я не знаю такого блока"
            return args_translator[arg]()
        msg = ""
        for val in args_translator.values():
            msg += f"{val()}\n\n"
        return msg

    def get_petrovich(self):
        players = PetrovichUser.objects \
            .filter(chat=self.vk_event.chat) \
            .filter(user__chats=self.vk_event.chat) \
            .order_by('-wins')
        msg = "Наши любимые Петровичи:\n"
        for player in players:
            msg += "%s - %s\n" % (player, player.wins)
        return msg

    def get_rates(self):
        gamers = Gamer.objects.filter(user__chats=self.vk_event.chat).exclude(points=0).order_by('-points')
        msg = "Победители ставок:\n"
        for gamer in gamers:
            msg += f"{gamer} - {gamer.points}\n"
        return msg

    def get_tic_tac_toe(self):
        gamers = Gamer.objects.filter(user__chats=self.vk_event.chat).exclude(tic_tac_toe_points=0).order_by(
            '-tic_tac_toe_points')
        msg = "Победители крестиков-ноликов:\n"
        for gamer in gamers:
            msg += f"{gamer} - {gamer.tic_tac_toe_points}\n"
        return msg

    def get_codenames(self):
        gamers = Gamer.objects.filter(user__chats=self.vk_event.chat).exclude(codenames_points=0).order_by(
            '-codenames_points')
        msg = "Победители коднеймса:\n"
        for gamer in gamers:
            msg += f"{gamer} - {gamer.codenames_points}\n"
        return msg

    def get_roulettes(self):
        gamers = Gamer.objects.filter(user__chats=self.vk_event.chat).exclude(roulette_points=0).order_by(
            '-roulette_points')
        msg = "Очки рулетки:\n"
        for gamer in gamers:
            msg += f"{gamer} - {gamer.roulette_points}\n"
        return msg

    def get_memes(self):
        users = VkUser.objects.filter(chats=self.vk_event.chat)

        result_list = list(
            Meme.objects.filter(author__in=users).values('author').annotate(total=Count('author')).order_by('-total'))
        msg = "Созданных мемов:\n"
        for result in result_list:
            msg += f"{users.get(id=result['author'])} - {result['total']}\n"
        return msg
