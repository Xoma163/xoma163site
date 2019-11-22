from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.models import PetrovichUser


class Statistics(CommonCommand):
    def __init__(self):
        names = ["стата", "статистика"]
        super().__init__(names, for_conversations=True)

    def start(self):
        players = PetrovichUser.objects.filter(chat_id=self.vk_event.chat_id).order_by('-wins')
        result_list = []
        for player in players:
            result_list.append([player, player.wins])

        msg = "Наши любимые Петровичи:\n"
        for result in result_list:
            msg += "%s - %s\n" % (result[0], result[1])
        self.vk_bot.send_message(self.vk_event.chat_id, msg)
