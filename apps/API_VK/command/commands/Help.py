from apps.API_VK.command.CommonCommand import CommonCommand


class Help(CommonCommand):
    def __init__(self):
        names = ["помощь", "хелп", "ман", "команды", "помоги", "памаги", "спаси", "хелб", "манул", "help", "start"]
        keyboard_user = {'text': 'Помощь', 'color': 'blue', 'row': 1, 'col': 2}
        super().__init__(names, keyboard_user=keyboard_user)

    def start(self):
        from apps.API_VK.command import COMMON_TEXTS, STUDENT_TEXTS, MODERATOR_TEXTS, ADMIN_TEXTS

        help_text = "\n— общие команды —\n"
        help_text += COMMON_TEXTS
        help_text += "\n"
        if self.vk_event.sender.is_student:
            help_text += "\n— команды для группы 6221 —\n"
            help_text += STUDENT_TEXTS
        if self.vk_event.sender.is_moderator:
            help_text += "\n— команды для модераторов —\n"
            help_text += MODERATOR_TEXTS
        if self.vk_event.sender.is_admin:
            help_text += "\n— команды для администраторов —\n"
            help_text += ADMIN_TEXTS

        return help_text
