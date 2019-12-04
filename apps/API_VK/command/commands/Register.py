from django.db.models import Min

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.models import PetrovichUser


class Register(CommonCommand):
    def __init__(self):
        names = ["регистрация", "рег"]
        help_text = "̲Р̲е̲г - регистрация для участия в петровиче дня"
        super().__init__(names, help_text, for_conversations=True)

    def start(self):
        vk_user = self.vk_bot.get_user_by_id(self.vk_event.user_id)
        if vk_user is not None:
            if PetrovichUser.objects.filter(user=vk_user, chat=self.vk_event.chat).first() is not None:
                self.vk_bot.send_message(self.vk_event.chat_id, "Ты уже зарегистрирован :)")
                return
        min_wins = PetrovichUser.objects.filter(chat=self.vk_event.chat).aggregate(Min('wins'))['wins__min']


        p_user = PetrovichUser()
        p_user.user = self.vk_event.sender
        p_user.chat = self.vk_event.chat
        if min_wins:
            p_user.wins = min_wins
        p_user.save()

        self.vk_bot.send_message(self.vk_event.chat_id, "Регистрация прошла успешно")
