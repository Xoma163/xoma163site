from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import get_one_chat_with_user
from apps.API_VK.models import VkUser, APITempUser, APIUser


def get_users(chat, who):
    params = {'chats': chat, 'groups__name': who}
    return list(VkUser.objects.filter(**params))


class APIChat(CommonCommand):
    def __init__(self):
        names = ["чат"]
        help_text = "Чат - привязывает чат к API"
        detail_help_text = "Чат - привязывает чат к API\n" \
                           "Чат привязать (название конфы) - отправляет код в выбранную конфу\n" \
                           "Чат отвязать (название конфы) - отправляет код в выбранную конфу\n" \
                           "Чат код (код) - привязывает чат к пользователю"
        super().__init__(names, help_text, detail_help_text, api=True, args=1)

    def start(self):
        if self.vk_event.sender.user_id == "ANONYMOUS":
            return "Анонимный пользователь не может иметь привязанных чатов"

        if self.vk_event.args[0] == 'привязать':
            self.check_args(2)
            chat_name = self.vk_event.original_args.split(' ', 1)[1]
            chat_with_user = get_one_chat_with_user(chat_name, self.vk_event.sender.user_id)

            APITempUser.objects.filter(user_id=self.vk_event.yandex['client_id']).delete()
            yandex_temp_user = APITempUser(
                user_id=self.vk_event.yandex['client_id'],
                vk_user=self.vk_event.sender,
                vk_chat=chat_with_user,
            )
            yandex_temp_user.save()
            msg = f"Код для пользователя {self.vk_event.sender}\n" \
                  f"{yandex_temp_user.code}"

            self.vk_bot.send_message(chat_with_user.chat_id, msg)
            return "Отправил код. Пришлите мне его. Чат код {код}"
        elif self.vk_event.args[0] == 'код':
            self.check_args(2)
            code = self.vk_event.args[1]
            yandex_temp_user = APITempUser.objects.filter(user_id=self.vk_event.yandex['client_id'],
                                                          vk_user=self.vk_event.sender,
                                                          vk_chat__isnull=False).first()
            if not yandex_temp_user:
                return "Не нашёл привязок. Привяжите /чат привязать {название конфы}"
            if yandex_temp_user.tries <= 0:
                return "Вы превысили максимальное число попыток"

            if yandex_temp_user.code != code:
                yandex_temp_user.tries -= 1
                yandex_temp_user.save()
                return f"Неверный код. Осталось попыток - {yandex_temp_user.tries}"

            yandex_users = APIUser.objects.filter(vk_user=yandex_temp_user.vk_user)
            if len(yandex_users) == 0:
                return "Не нашёл пользователя APIUser, оч странная хрень. Напишите разрабу"
            for yandex_user in yandex_users:
                yandex_user.vk_chat = yandex_temp_user.vk_chat
                yandex_user.save()
            yandex_temp_user.delete()
            return "Успешно привязал"
        elif self.vk_event.args[0] == 'отвязать':
            yandex_users = APIUser.objects.filter(vk_user=self.vk_event.sender)
            if len(yandex_users) == 0:
                return "Не нашёл пользователя APIUser, оч странная хрень. Напишите разрабу"
            for yandex_user in yandex_users:
                yandex_user.vk_chat = None
                yandex_user.save()
            return "Успешно отвязал"
        else:
            return "Не понял. Доступно: Чат привязать/код/отвязать."
