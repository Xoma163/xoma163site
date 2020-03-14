from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.models import VkUser, YandexTempUser


class VkontakteYandex(CommonCommand):
    def __init__(self):
        names = ["вк", "вконтакте", "ъуъ"]
        help_text = "вк - регистрация пользователя в Алисе"
        super().__init__(names,
                         help_text,
                         # api=True,
                         args=1)

    def start(self):
        if self.vk_event.args[0] == "код":
            pass
        else:
            self.int_args = [0]
            self.parse_args('int')
            user_id = int(self.vk_event.args[0])
            vk_user = VkUser.objects.filter(user_id=user_id).first()
            if vk_user:

                yandex_temp_user = YandexTempUser.objects.filter(vk_user=vk_user).first()
                if yandex_temp_user:
                    self.vk_bot.send_message(vk_user.user_id, yandex_temp_user.code)
                    return "Отправил код повторно"
                else:
                    yandex_temp_user = YandexTempUser(vk_user=vk_user, user_id='123456678')
                    yandex_temp_user.save()
                    self.vk_bot.send_message(vk_user.user_id, yandex_temp_user.code)
                    return "Отправил код подтверждения в ВК. Пришлите мне его"
            else:
                return "Вы не зарегистрированы. Напишите боту любое сообщение"
        return None
