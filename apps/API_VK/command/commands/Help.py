from apps.API_VK.command.CommonCommand import CommonCommand


def get_help_for_command(help_command):
    from apps.API_VK.command import get_commands
    commands = get_commands()

    found_command = None
    for command in commands:

        if command.names and help_command in command.names:
            found_command = command
            break

    if found_command:
        if found_command.detail_help_text:
            return found_command.detail_help_text
        else:
            return "У данной команды нет подробного описания"
    else:
        return "Я не знаю такой команды"


class Help(CommonCommand):
    def __init__(self):
        names = ["помощь", "хелп", "ман", "команды", "помоги", "памаги", "спаси", "хелб", "манул", "help", "start"]
        detail_help_text = "Ты дебил?"
        keyboard = {'text': 'Помощь', 'color': 'blue', 'row': 1, 'col': 2}
        super().__init__(names, keyboard=keyboard, detail_help_text=detail_help_text)

    def start(self):
        if self.vk_event.args:
            return get_help_for_command(self.vk_event.args[0].lower())
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
