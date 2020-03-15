from apps.API_VK.command.CommonCommand import CommonCommand


class Conference(CommonCommand):
    def __init__(self):
        names = ["конфа", "конференция", "беседа"]

        super().__init__(names, conversation=True)

    def accept(self, vk_event):
        if vk_event.chat and (vk_event.chat.name is None or vk_event.chat.name == "") or vk_event.command in self.names:
            return True
        return False

    def start(self):
        if self.vk_event.command in self.names:
            if self.vk_event.args:
                self.vk_event.chat.name = self.vk_event.original_args
                self.vk_event.chat.save()
            else:
                if self.vk_event.chat.name and self.vk_event.chat.name != "":
                    return self.vk_event.chat.name
                else:
                    return "Конфа не имеет названия"
            return f"Поменял название беседы на {self.vk_event.original_args}"
        else:
            return "Не задано имя конфы, задайте его командой /конфа 'Название конфы'"
