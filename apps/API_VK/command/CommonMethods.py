import json
import random
import re
import threading

import pytz


def get_random_item_from_list(my_list, arg=None):
    rand_int = random.randint(0, len(my_list) - 1)
    if arg:
        msg = f"{arg}, ты {my_list[rand_int].lower()}"
    else:
        msg = my_list[rand_int]
    return msg


# Вероятность события в процентах
def random_probability(probability):
    if 1 > probability > 99:
        raise RuntimeError("Вероятность события должна быть от 1 до 99")
    rand_int = random.randint(1, 100)
    if rand_int <= probability:
        return True
    else:
        return False


# Возвращает случайное событие с указанными весами этих событий
def random_event(events, weights):
    # В принципе это необязательно
    if sum(weights) != 100:
        raise RuntimeError("Сумма вероятности событий должна равняться 100")
    return random.choices(events, weights=weights)


# Есть ли кириллица
def has_cyrillic(text):
    return bool(re.search('[а-яА-Я]', text))


# Проверить вхождение пользователя в группу
def check_user_group(user, role):
    group = user.groups.filter(name=role)
    return group.exists()


# Получить все группы пользователя
def get_user_groups(user):
    groups = user.groups.all().values()
    return [group['name'] for group in groups]


def _send_messages_thread(vk_bot, users, message):
    for user in users:
        vk_bot.parse_and_send_msgs(user.user_id, message)


# Отправляет сообщения в потоке всем пользователям
def send_messages(vk_bot, users, message):
    thread = threading.Thread(target=_send_messages_thread, args=(vk_bot, users, message,))
    thread.start()


# Убирает временную зону у datetime
def remove_tz(datetime):
    return datetime.replace(tzinfo=None)


def localize_datetime(datetime, tz):
    tz_obj = pytz.timezone(tz)
    return pytz.utc.localize(datetime, is_dst=None).astimezone(tz_obj)


def normalize_datetime(datetime, tz):
    tz_obj = pytz.timezone(tz)
    localized_time = tz_obj.localize(datetime, is_dst=None)

    tz_utc = pytz.timezone("UTC")
    return pytz.utc.normalize(localized_time, is_dst=None).astimezone(tz_utc)  # .replace(tzinfo=None)


# Возвращает чат по названию, где есть пользователь
def get_one_chat_with_user(chat_name, user_id):
    from apps.API_VK.models import VkChat
    chats = VkChat.objects.filter(name__icontains=chat_name)
    if len(chats) == 0:
        raise RuntimeError("Не нашёл такого чата")

    chats_with_user = []
    for chat in chats:
        user_contains = chat.vkuser_set.filter(user_id=user_id)
        if user_contains:
            chats_with_user.append(chat)

    if len(chats_with_user) == 0:
        raise RuntimeError("Не нашёл доступного чата с пользователем в этом чате")
    elif len(chats_with_user) > 1:
        chats_str = '\n'.join(chats_with_user)
        raise RuntimeError("Нашёл несколько чатов. Уточните какой:\n"
                           f"{chats_str}")

    elif len(chats_with_user) == 1:
        return chats_with_user[0]


# Возвращает упоминание пользователя
def get_mention(user, name=None):
    if not name:
        name = user.name
    return f"[id{user.user_id}|{name}]"


# Склоняет существительное после числительного
# number - число, titles - 3 склонения.
def decl_of_num(number, titles):
    cases = [2, 0, 1, 1, 1, 2]
    if 4 < number % 100 < 20:
        return titles[2]
    elif number % 10 < 5:
        return titles[cases[number % 10]]
    else:
        return titles[cases[5]]


# Получает вложения и загружает необходимые на сервер, на которых нет прав
# Прикрепляет только фото, видео, аудио и документы.
# ToDo: придумать как обрабатывать посты или ссылки
def get_attachments_for_upload(vk_bot, attachments):
    uploaded_attachments = []
    for attachment in attachments:
        # Фото
        if attachment['type'] == 'photo':
            new_attachment = vk_bot.upload_photo(attachment['download_url'])
            uploaded_attachments.append(new_attachment)
        # Видео, аудио, документы
        elif 'vk_url' in attachment:
            uploaded_attachments.append(attachment['vk_url'])
    return uploaded_attachments


# Получает все вложения из сообщения и пересланного сообщения
def get_attachments_from_attachments_or_fwd(vk_event, _type):
    if _type is str:
        _type = [_type]
    from apps.API_VK.VkBotClass import parse_attachments
    attachments = []
    if vk_event.attachments:
        for att in vk_event.attachments:
            if att['type'] in _type:
                attachments.append(att)
    if vk_event.fwd:
        msg = vk_event.fwd[0]
        if msg['attachments']:
            fwd_attachments = parse_attachments(msg['attachments'])
            for att in fwd_attachments:
                if att['type'] in _type:
                    attachments.append(att)

    return attachments


# Возвращает клавиатуру с кнопкой "Ещё"
def get_inline_keyboard(command_text, button_text="Ещё", args=None):
    if args is None:
        args = {}
    return {
        'inline': True,
        'buttons': [[
            {
                'action': {
                    'type': 'text',
                    'label': button_text,
                    "payload": json.dumps({"command": command_text, "args": args}, ensure_ascii=False)
                },
                'color': 'primary',
            }
        ]]}


# Ищет команду по имени
def find_command_by_name(command_name):
    from apps.API_VK.command import get_commands
    commands = get_commands()

    for command in commands:
        if command.names and command_name in command.names:
            return command
    return None


# Получает detail_help_text для команды
def get_help_for_command(command):
    if command.detail_help_text:
        return command.detail_help_text
    else:
        return "У данной команды нет подробного описания"
