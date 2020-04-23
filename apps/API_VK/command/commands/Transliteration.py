import transliterate

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import has_cyrillic


def get_en_transliterate(msg):
    return transliterate.translit(msg, reversed=True)


def get_ru_transliterate(msg):
    return transliterate.translit(msg, 'ru')


class Transliteration(CommonCommand):
    def __init__(self):
        names = ["транслит"]
        help_text = "Транслит - автоматическая транслитерация"
        detail_help_text = "Транслит (Текст/Пересланные сообщения) - в зависимости от фразы транслитит на нужный " \
                           "язык(английский или русский)"
        super().__init__(names, help_text, detail_help_text)

    def start(self):
        msgs = self.vk_event.fwd
        if not msgs:
            if not self.vk_event.original_args:
                return "Требуется аргументы или пересылаемые сообщения"

            msgs = [{'text': self.vk_event.original_args, 'from_id': int(self.vk_event.sender.user_id)}]
        translite_text = ""
        for msg in msgs:
            text = msg['text']
            translite_text += f"{text}\n\n"

        if has_cyrillic(translite_text):
            return get_en_transliterate(translite_text)
        else:
            return get_ru_transliterate(translite_text)
