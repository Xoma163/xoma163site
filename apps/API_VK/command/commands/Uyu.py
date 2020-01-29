from apps.API_VK.command.CommonCommand import CommonCommand


# ToDo: add_word должна быть не только словом, но и фразой
class Uyu(CommonCommand):
    def __init__(self):
        names = ["уъу", "бля", "ъуъ"]
        help_text = "Уъу - уъуфикация текста"
        detail_help_text = "Уъу ([N]) - уъуфикация текста. Для работы требует пересылаемое сообщение. Если передан аргумент, то слово поменяется"
        super().__init__(names, help_text, detail_help_text)

    def start(self):
        if self.vk_event.original_args:
            add_word = self.vk_event.original_args
        else:
            add_word = "бля"
        msgs = self.vk_event.fwd
        print(self.vk_event.fwd)
        if msgs is None:
            return add_word
        if len(msgs) == 1:
            new_msg = msgs[0]['text']
        else:
            new_msg = ""
            for msg in msgs:
                new_msg += msg['text'] + "\n"
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
