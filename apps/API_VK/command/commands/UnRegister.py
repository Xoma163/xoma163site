from apps.API_VK.command.CommonCommand import CommonCommand
from apps.games.models import PetrovichUser


class UnRegister(CommonCommand):
    def __init__(self):
        names = ["дерегистрация", "дерег"]
        help_text = "Дерег - отказ участия в петровиче дня"
        super().__init__(names, help_text, conversation=True)

    def start(self):
        p_user = PetrovichUser.objects.filter(user=self.vk_event.sender, chat=self.vk_event.chat).first()
        if p_user is not None:
            p_user.active = False
            p_user.save()
            return "Ок"
        else:
            return "А ты и не зареган"
