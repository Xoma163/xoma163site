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
        from apps.API_VK.command import HELP_TEXT, API_HELP_TEXT

        if self.vk_event.api:
            help_texts = API_HELP_TEXT
        else:
            help_texts = HELP_TEXT
        output = "\n— общие команды —\n"
        output += help_texts['user']
        output += "\n"
        if self.vk_event.sender.is_student:
            output += "\n— команды для группы 6221 —\n"
            output += help_texts['student']
        if self.vk_event.sender.is_moderator:
            output += "\n— команды для модераторов —\n"
            output += help_texts['moderator']
        if self.vk_event.sender.is_admin:
            output += "\n— команды для администраторов —\n"
            output += help_texts['admin']

        return output
