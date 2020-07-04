import random
import threading

import telebot

from apps.API_TG.models import TgUser, TgTempUser
from apps.API_VK.VkBotClass import VkBotClass
from apps.API_VK.VkEvent import VkEvent
from apps.API_VK.models import VkUser
from secrets.secrets import secrets

token = secrets['telegram']['key']
bot = telebot.TeleBot(token)


def register_and_confirm(message, tg_user):
    msg_list = message.split(' ')
    for i, _ in enumerate(msg_list):
        msg_list[i] = msg_list[i].lower()
    if msg_list and len(msg_list) >= 2:
        if msg_list[0] == 'вк':
            return register(message.split(' ', 1)[1], tg_user)
        elif msg_list[0] == 'код':
            return confirm(message.split(' ', 1)[1], tg_user)
    return "Вы не зарегистрированны. Пришлите ВК {ваш ид}"


def register(vk_id, tg_user):
    vk_id = vk_id.replace('-', '').replace(' ', '')
    user_id = int(vk_id)
    vk_user = VkUser.objects.filter(user_id=user_id).first()
    if vk_user:
        tg_temp_user = TgTempUser.objects.filter(vk_user=vk_user, tg_user=tg_user).first()
        vk_bot = VkBotClass()
        if tg_temp_user:
            vk_bot.send_message(vk_user.user_id, tg_temp_user.code)
            return "Отправил код повторно"
        else:
            tg_temp_user = TgTempUser(vk_user=vk_user, tg_user=tg_user)
            tg_temp_user.save()
            vk_bot.send_message(vk_user.user_id, tg_temp_user.code)
            return "Отправил код подтверждения в ВК. Пришлите мне его. Код {код}"
    else:
        return "Вы не зарегистрированы. Напишите боту в ВК любое сообщение"


def confirm(code, tg_user):
    code = code.replace('-', '').replace(' ', '')

    tg_temp_user = TgTempUser.objects.filter(tg_user=tg_user).first()
    if not tg_temp_user:
        return "Вы не зарегистрированны. Пришлите ВК {ваш ид}"
    if tg_temp_user.tries <= 0:
        return "Вы превысили максимальное число попыток"
    if tg_temp_user.code != code:
        tg_temp_user.tries -= 1
        tg_temp_user.save()
        return f"Неверный код. Осталось попыток - {tg_temp_user.tries}"
    tg_user.vk_user = tg_temp_user.vk_user
    tg_user.save()
    tg_temp_user.delete()
    return "Успешно зарегистрировал. Можете пользоваться функционалом"


class TgBotClass(threading.Thread):
    def __init__(self):
        super().__init__()

        self._token = token
        self.bot = bot

    def run(self):
        bot.polling(none_stop=True)

    @staticmethod
    def get_random_code(length=6):
        return str(random.randint(10 ** (length - 1), 10 ** length - 1))

    @staticmethod
    @bot.message_handler(content_types=["text"])
    def all_messages(message):
        try:
            tg_user, _ = TgUser.objects.get_or_create(user_id=message.from_user.id)
            if not tg_user.is_active():
                res = register_and_confirm(message.text, tg_user)
                bot.send_message(message.chat.id, res)
                return

            msg = message.text
            if msg.startswith('/'):
                msg = message.text[1:]

            vk_event = {
                'message': {
                    'text': msg
                },
                'sender': tg_user.vk_user,
                'chat': None,
                'peer_id': tg_user.vk_user.user_id,

                'api': True
            }

            vk_event_object = VkEvent(vk_event)
            vk_bot = VkBotClass()
            result = vk_bot.menu(vk_event_object, send=False)

            bot.send_message(message.chat.id, result)
        except:
            bot.send_message(message.chat.id, "Произошла ошибка. Напишите разработчику, что случилось((")
