from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import has_cyrillic

_eng_chars = u"~`!@#$%^&qwertyuiop[]asdfghjkl;'zxcvbnm,./QWERTYUIOP{}ASDFGHJKL:\"|ZXCVBNM<>?"
_rus_chars = u"ёё!\"№;%:?йцукенгшщзхъфывапролджэячсмитьбю.ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭ/ЯЧСМИТЬБЮ,"
_trans_table = dict(zip(_eng_chars, _rus_chars))
_trans_table_reverse = dict(zip(_rus_chars, _eng_chars))


def fix_layout(s, reverse):
    if not reverse:
        return u''.join([_trans_table.get(c, c) for c in s])
    else:
        return u''.join([_trans_table_reverse.get(c, c) for c in s])


class Fix(CommonCommand):
    def __init__(self):
        names = ["фикс", "раскладка"]
        help_text = "Фикс - исправляет раскладку текста"
        detail_help_text = "Фикс (Пересылаемые сообщения) - исправляет раскладку текста"
        super().__init__(names, help_text, detail_help_text, fwd=True, api=False)

    def start(self):
        msgs = ""
        for msg in self.vk_event.fwd:
            if msg['text']:
                msgs += f"{fix_layout(msg['text'], has_cyrillic(msg['text']))}\n"
        if not msgs:
            return "Нет текста в сообщении или пересланных сообщениях"
        return msgs
