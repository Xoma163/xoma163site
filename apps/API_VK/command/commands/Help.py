from apps.API_VK.command.CommonCommand import CommonCommand


class Help(CommonCommand):
    def __init__(self):
        names = ["помощь", "хелп", "ман", "команды", "помоги", "памаги", "спаси", "хелб", "манул", "help", "start"]
        keyboard = {'text': 'Помощь', 'color': 'blue', 'row': 1, 'col': 2}
        super().__init__(names, keyboard=keyboard)

    def start(self):
        from apps.API_VK.command import HELP_TEXTS
        help_text = "\n— общие команды —\n"
        help_text += HELP_TEXTS['user']
        help_text += "\n"
        if self.vk_event.sender.is_student:
            help_text += "\n— команды для группы 6221 —\n"
            help_text += HELP_TEXTS['student']
        if self.vk_event.sender.is_moderator:
            help_text += "\n— команды для модераторов —\n"
            help_text += HELP_TEXTS['moderator']
        if self.vk_event.sender.is_admin:
            help_text += "\n— команды для администраторов —\n"
            help_text += HELP_TEXTS['admin']

        return help_text
