from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import check_user_group


def get_help_for_command(help_command):
    from apps.API_VK.command import get_commands
    commands = get_commands()

    for command in commands:

        if command.names and help_command in command.names:
            if command.detail_help_text:
                return command.detail_help_text
            else:
                return "У данной команды нет подробного описания"
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

        if self.vk_event.from_api:
            help_texts = API_HELP_TEXT
        else:
            help_texts = HELP_TEXT
        output = "— общие команды —\n"
        output += help_texts['user']

        if check_user_group(self.vk_event.sender, 'student') and help_texts['student']:
            output += "\n\n— команды для группы 6221 —\n"
            output += help_texts['student']
        if check_user_group(self.vk_event.sender, 'moderator') and help_texts['moderator']:
            output += "\n\n— команды для модераторов —\n"
            output += help_texts['moderator']
        if check_user_group(self.vk_event.sender, 'admin') and help_texts['admin']:
            output += "\n\n— команды для администраторов —\n"
            output += help_texts['admin']
        if check_user_group(self.vk_event.sender, 'banned') and help_texts['banned']:
            output += "\n\n— команды для забаненных —\n"
            output += help_texts['banned']
        if check_user_group(self.vk_event.sender, 'minecraft') and help_texts['minecraft']:
            output += "\n\n— команды для игроков майнкрафта —\n"
            output += help_texts['minecraft']
        if check_user_group(self.vk_event.sender, 'minecraft_notify') and help_texts['minecraft_notify']:
            output += "\n\n— команды для уведомлённых майнкрафтеров —\n"
            output += help_texts['minecraft_notify']
        if check_user_group(self.vk_event.sender, 'terraria') and help_texts['terraria']:
            output += "\n\n— команды для игроков террарии —\n"
            output += help_texts['terraria']

        return output
