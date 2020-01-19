from apps.API_VK.command.CommonCommand import CommonCommand


class Conference(CommonCommand):
    def __init__(self):
        names = ["конфа", "конференция", "беседа", "чат"]

        super().__init__(names, for_conversations=True)

    def accept(self, vk_event):
        if vk_event.chat and (vk_event.chat.name is None or vk_event.chat.name == ""):
            return True
        return False

    def start(self):

        if self.vk_event.command in self.names:
            self.need_args = 1
            self.check_args()
            self.vk_event.chat.name = self.vk_event.args[0]
            self.vk_event.chat.save()
            return f"Поменял название беседы на {self.vk_event.args[0]}"
        else:
            return "Не задано имя конфы, задайте его командой /конфа 'Название конфы'"
