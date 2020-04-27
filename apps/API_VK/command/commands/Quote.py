from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.models import QuoteBook


class Quote(CommonCommand):
    def __init__(self):
        names = ["цитата", "(c)", "(с)"]
        help_text = "Цитата - сохраняет в цитатник сообщения"
        detail_help_text = "Цитата (Пересылаемые сообщение) - сохраняет в цитатник сообщения"
        super().__init__(names, help_text, detail_help_text, fwd=True)

    def start(self):
        msgs = self.vk_event.fwd

        quote = QuoteBook()
        quote_text = ""
        for msg in msgs:
            text = msg['text']
            if msg['from_id'] > 0:
                quote_user_id = int(msg['from_id'])
                quote_user = self.vk_bot.get_user_by_id(quote_user_id)
                username = quote_user.name + " " + quote_user.surname
            else:
                quote_bot_id = int(msgs[0]['from_id'])
                quote_bot = self.vk_bot.get_bot_by_id(quote_bot_id)
                username = quote_bot.name
            quote_text += f"{username}:\n{text}\n\n"
        quote.text = quote_text
        if self.vk_event.chat:
            quote.vk_chat = self.vk_event.chat
        else:
            quote.vk_user = self.vk_event.sender
        quote.save()
        return "Цитата сохранена"
