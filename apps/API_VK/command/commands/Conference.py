from apps.API_VK.command.CommonCommand import CommonCommand


class Conference(CommonCommand):
    def __init__(self):
        names = ["конфа", "конференция", "беседа", "чат"]

        super().__init__(names, conversation=True)

    def accept(self, vk_event):
        if vk_event.chat and (vk_event.chat.name is None or vk_event.chat.name == "") or vk_event.command in self.names:
            return True
        return False

    def start(self):

        if self.vk_event.command in self.names:
            self.check_args(1)
            self.vk_event.chat.name = self.vk_event.args[0]
            self.vk_event.chat.save()
            return f"Поменял название беседы на {self.vk_event.args[0]}"
        else:
            return "Не задано имя конфы, задайте его командой /конфа 'Название конфы'"
