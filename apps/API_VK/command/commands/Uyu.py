from apps.API_VK.command.CommonCommand import CommonCommand


class Uyu(CommonCommand):
    def __init__(self):
        names = ["уъу", "бля", "ъуъ"]
        super().__init__(names, check_fwd=True)

    def start(self):

        add_word = "бля"
        msgs = self.vk_event.fwd

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
        self.vk_bot.send_message(self.vk_event.chat_id, new_msg)
