from apps.API_VK.command.CommonCommand import CommonCommand


class Debug(CommonCommand):
    def __init__(self):
        names = ["дебаг"]
        help_text = "Дебаг - отображение распаршенного сообщения"
        super().__init__(names, help_text, access='moderator')

    def start(self):
        self.vk_bot.DEBUG = not self.vk_bot.DEBUG

        if self.vk_bot.DEBUG:
            return 'Включил'
        else:
            return 'Выключил'
