from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.models import VkUser, VkChat, YandexTempUser, YandexUser


def get_users(chat, who):
    params = {'chats': chat, 'groups__name': who}
    return list(VkUser.objects.filter(**params))


class YandexChat(CommonCommand):
    def __init__(self):
        names = ["чат"]
        help_text = "Чат - привязывает чат к API"
        detail_help_text = "Чат - привязывает чат к API.\n" \
                           "Чат привязать {название конфы} - отправляет код в выбранную конфу\n" \
                           "Чат код {код} - привязывает чат к пользователю"
        super().__init__(names, help_text, detail_help_text, api=True, args=1)

    def start(self):
        if self.vk_event.args[0] == 'привязать':
            chat_name = self.vk_event.original_args.split(' ', 1)[1]
            chats = VkChat.objects.filter(name__icontains=chat_name)
            if len(chats) == 0:
                return "Не нашёл такого чата"

            chats_with_user = []
            for chat in chats:
                user_contains = chat.vkuser_set.filter(user_id=self.vk_event.sender.user_id)
                if user_contains:
                    chats_with_user.append(chat)

            if len(chats_with_user) == 0:
                return "Не нашёл доступного чата с пользователем в этом чате"
            elif len(chats_with_user) > 1:
                chats_str = '\n'.join(chats_with_user)
                return "Нашёл несколько чатов. Уточните какой:\n" \
                       f"{chats_str}"
            elif len(chats_with_user) == 1:
                chat_with_user = chats_with_user[0]
                YandexTempUser.objects.filter(user_id=self.vk_event.yandex['client_id']).delete()
                yandex_temp_user = YandexTempUser(
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
            code = self.vk_event.args[1]
            yandex_temp_user = YandexTempUser.objects.filter(user_id=self.vk_event.yandex['client_id'],
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

            yandex_users = YandexUser.objects.filter(vk_user=yandex_temp_user.vk_user)
            if len(yandex_users) == 0:
                return "Не нашёл пользователя YandexUser, оч странная хрень. Напишите разрабу"
            for yandex_user in yandex_users:
                yandex_user.vk_chat = yandex_temp_user.vk_chat
                yandex_user.save()
            yandex_temp_user.delete()
            return "Успешно привязал"
        elif self.vk_event.args[0] == 'отвязать':
            yandex_users = YandexUser.objects.filter(vk_user=self.vk_event.sender)
            if len(yandex_users) == 0:
                return "Не нашёл пользователя YandexUser, оч странная хрень. Напишите разрабу"
            for yandex_user in yandex_users:
                yandex_user.vk_chat = None
                yandex_user.save()
            return "Успешно отвязал"
        else:
            return "Не понял. Доступно: Чат привязать/код/отвязать."
        return
