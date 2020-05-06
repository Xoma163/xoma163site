from enum import Enum


class Role(Enum):
    ADMIN = "администратор"
    CONFERENCE_ADMIN = "админ конфы"
    MODERATOR = "модератор"
    MINECRAFT = "майнкрафт"
    TERRARIA = "террария"
    STUDENT = "студент"
    MINECRAFT_NOTIFY = "уведомления майна"
    USER = "пользователь"
    BANNED = "забанен"
    TRUSTED = "доверенный"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


week_translator = {
    'понедельник': 1, 'пн': 1,
    'вторник': 2, 'вт': 2,
    'среда': 3, 'ср': 3,
    'четверг': 4, 'чт': 4,
    'пятница': 5, 'пт': 5,
    'суббота': 6, 'сб': 6,
    'воскресенье': 7, 'воскресение': 7, 'вс': 7,
}

on_off_translator = {
    'on': True,
    'вкл': True,
    '1': True,
    'true': True,
    'включить': True,
    'включи': True,
    'вруби': True,

    'off': False,
    'выкл': False,
    '0': False,
    'false': False,
    'выключить': False,
    'выключи': False,
    'выруби': False
}
