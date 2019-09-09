# TELEGRAM_BOT_API
# ToDo: Сделать вебхуки и меню в телеграмме, чтобы можно было общаться с ботом
import threading


class TBot:

    def __init__(self):
        import telebot
        from telebot import apihelper

        from xoma163site.settings import BASE_DIR

        f = open(BASE_DIR + "/secrets/telegram_bot.txt", "r")

        proxy_url = 'socks5h://192.169.215.114:44598'
        api_token = f.readline().replace('\r', '').replace('\n', '')
        # self.XOMA163_CHAT_ID = int(f.readline())
        # self.LANA_CHAT_ID = int(f.readline())

        f.close()

        apihelper.proxy = {'https': proxy_url}
        # ToDo: меню бота
        # @self.bot.message_handler(commands=['start', 'help'])
        # def send_welcome(message):
        #     self.bot.reply_to(message, "Howdy, how are you doing?")
        #
        # @self.bot.message_handler(func=lambda message: True)
        # def echo_all(message):
        #     self.bot.reply_to(message, message.text)

        self.bot = telebot.TeleBot(api_token)
        # threading.Thread(target=self.bot.polling, args=(), daemon=True).join()




        #
