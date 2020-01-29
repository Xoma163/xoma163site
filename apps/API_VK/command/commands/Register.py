from django.db.models import Min

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.games.models import PetrovichUser


class Register(CommonCommand):
    def __init__(self):
        names = ["регистрация", "рег"]
        help_text = "Рег - регистрация для участия в петровиче дня"
        super().__init__(names, help_text, for_conversations=True)

    def start(self):
        p_user = PetrovichUser.objects.filter(user=self.vk_event.sender, chat=self.vk_event.chat).first()
        if p_user is not None:
            if not p_user.active:
                p_user.active = True
                p_user.save()
                return "Возвращаю тебя в строй"
            else:
                return "Ты уже зарегистрирован :)"
        min_wins = PetrovichUser.objects.filter(chat=self.vk_event.chat).aggregate(Min('wins'))['wins__min']

        p_user = PetrovichUser()
        p_user.user = self.vk_event.sender
        p_user.chat = self.vk_event.chat
        p_user.active = True
        if min_wins:
            p_user.wins = min_wins
        p_user.save()

        return "Регистрация прошла успешно"
