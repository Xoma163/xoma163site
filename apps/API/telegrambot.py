# TELEGRAM_BOT_API

class TBot:

    def __init__(self):
        import telebot
        from telebot import apihelper

        from xoma163site.settings import BASE_DIR

        f = open(BASE_DIR + "/secrets/telegram_bot.txt", "r")

        proxy_url = 'socks5h://192.169.215.114:44598'
        api_token = f.readline().replace('\r', '').replace('\n', '')
        self.XOMA163_CHAT_ID = int(f.readline())
        self.LANA_CHAT_ID = int(f.readline())

        f.close()

        apihelper.proxy = {'https': proxy_url}

        self.bot = telebot.TeleBot(api_token)
        # bot.polling()
