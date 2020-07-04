from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.Consts import Role
from apps.API_VK.models import VkChat


class Conference(CommonCommand):
    def __init__(self):
        names = ["конфа", "конференция", "беседа"]
        help_text = "Конфа - назвать конфу"
        super().__init__(names, help_text, conversation=True, priority=90, api=False)

    def accept(self, vk_event):
        if vk_event.chat and (vk_event.chat.name is None or vk_event.chat.name == "") or vk_event.command in self.names:
            return True

        return False

    def start(self):
        if self.vk_event.command in self.names:
            if self.vk_event.args:
                try:
                    self.check_sender(Role.CONFERENCE_ADMIN)
                    same_chats = VkChat.objects.filter(name=self.vk_event.original_args)
                    if len(same_chats) > 0:
                        return "Конфа с таким названием уже есть. Придумайте другое"
                    self.vk_event.chat.name = self.vk_event.original_args
                    self.vk_event.chat.save()
                    return f"Поменял название беседы на {self.vk_event.original_args}"
                except RuntimeError as e:
                    if self.vk_event.chat.admin is None:
                        msg = "Так как администратора конфы не было, то теперь вы стали администратором конфы!"
                        self.vk_event.chat.admin = self.vk_event.sender
                        same_chats = VkChat.objects.filter(name=self.vk_event.original_args)
                        if len(same_chats) > 0:
                            msg += "\nКонфа с таким названием уже есть. Придумайте другое"
                            return msg
                        self.vk_event.chat.name = self.vk_event.original_args
                        self.vk_event.chat.save()
                        msg += f"\nПоменял название беседы на {self.vk_event.original_args}"
                        return msg
                    else:
                        return str(e)

            else:
                if self.vk_event.chat.name and self.vk_event.chat.name != "":
                    return f"Название конфы - {self.vk_event.chat.name}"
                else:
                    return "Конфа не имеет названия"
        else:
            return "Не задано имя конфы, задайте его командой /конфа (название конфы)"
