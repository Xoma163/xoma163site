from apps.API_VK.command.CommonCommand import CommonCommand


class Conference(CommonCommand):
    def __init__(self):
        names = ["конфа", "конференция", "беседа", "чат"]

        super().__init__(names, need_args=1, for_conversations=True)

    def start(self):
        print('123')
        print(self.vk_event.chat, '123')
        self.vk_event.chat.name = self.vk_event.args[0]
        self.vk_event.chat.save()
        return f"Поменял название беседы на {self.vk_event.args[0]}"
