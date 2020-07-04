from apps.API_VK.command.CommonCommand import CommonCommand


class Uyu(CommonCommand):
    def __init__(self):
        names = ["уъу", "ъуъ"]
        help_text = "Уъу - Добавляет слово в текст (уъуфикация)"
        detail_help_text = "Уъу (Пересланные сообщения) [новое слово=бля] - добавляет слово в текст (уъуфикация)"
        super().__init__(names, help_text, detail_help_text, api=False)

    def start(self):
        add_word = "бля"
        if self.vk_event.original_args:
            add_word = self.vk_event.original_args

        msgs = self.vk_event.fwd
        if msgs is None:
            return add_word
        new_msg = ""
        for msg in msgs:
            if msg['text']:
                new_msg += msg['text'] + "\n"

        new_msg = new_msg.strip()
        if not new_msg:
            return "Нет текста в сообщении или пересланных сообщениях"

        symbols_first_priority = ['...']
        symbols_left = ['.', ',', '?', '!', ':']
        symbols_right = [' —', ' -']
        flag = False
        if new_msg[-1] not in symbols_left:
            new_msg += '.'
            flag = True
        for symbol in symbols_first_priority:
            new_msg = new_msg.replace(symbol, " " + add_word + symbol)
        for symbol in symbols_left:
            new_msg = new_msg.replace(symbol, " " + add_word + symbol)
        for symbol in symbols_right:
            new_msg = new_msg.replace(symbol, " " + add_word + " " + symbol)
        if flag:
            new_msg = new_msg[:-1]
        return new_msg
