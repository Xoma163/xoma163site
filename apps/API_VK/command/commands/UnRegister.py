from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.models import PetrovichUser


class UnRegister(CommonCommand):
    def __init__(self):
        names = ["дерегистрация", "дерег"]
        help_text = "̲Д̲е̲р̲е̲г - отказ участия в петровиче дня"
        super().__init__(names, help_text, for_conversations=True)

    def start(self):
        vk_user = self.vk_bot.get_user_by_id(self.vk_event.user_id)
        p_user = PetrovichUser.objects.filter(user=vk_user, chat=self.vk_event.chat).first()
        if p_user is not None:
            p_user.active = False
            self.vk_bot.send_message(self.vk_event.chat_id, "Ок")
            p_user.save()
            return
        else:
            self.vk_bot.send_message(self.vk_event.chat_id, "А ты и не зареган")
            return
