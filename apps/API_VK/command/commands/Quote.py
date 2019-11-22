from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.models import QuoteBook


class Quote(CommonCommand):
    def __init__(self):
        names = ["цитата", "(c)", "(с)"]
        super().__init__(names, check_fwd=True)

    def start(self):
        msgs = self.vk_event.fwd

        quote = QuoteBook()
        quote.peer_id = self.vk_event.peer_id
        quote_text = ""
        for msg in msgs:
            text = msg['text']
            if msg['from_id'] > 0:
                quote.user_id = int(msg['from_id'])
                quote_user = self.vk_bot.get_user_by_id(quote.user_id, self.vk_event.chat_id)
                username = quote_user.name + " " + quote_user.surname
            else:
                quote.user_id = int(msgs[0]['from_id']) * (-1)
                quote_bot = self.vk_bot.get_bot_by_id(quote.user_id)
                username = quote_bot.name
            quote_text += "{}:\n{}\n\n".format(username, text)
        quote.text = quote_text
        quote.save()
        self.vk_bot.send_message(self.vk_event.chat_id, "Цитата сохранена")
