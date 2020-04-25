from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import check_user_group, find_command_by_name, get_help_for_command


class Help(CommonCommand):
    def __init__(self):
        names = ["помощь", "хелп", "ман", "команды", "помоги", "памаги", "спаси", "хелб", "манул", "help", "start"]
        detail_help_text = "Формат детальной помощи по командам:\n" \
                           "Команда - выполняет команду\n" \
                           "Команда параметр - выполняет команду с параметром\n" \
                           "Команда (аргумент) - выполняет команду с обязательным аргументом\n" \
                           "Команда [аргумент=10] - выполняет команду с необязательным аргументов. Если не указать " \
                           "его, будет подставлено значение по умолчанию\n\n" \
                           "Формальный вывод команды:\n" \
                           "Команда параметр (аргумент) [необязательный аргумент 1 [необязательный аргумент 2 при " \
                           "условии передачи первого аргумента]] [необязательный аргумент 3 со значением по умолчанию 20=20]"

        keyboard = {'text': 'Помощь', 'color': 'blue', 'row': 1, 'col': 2}
        super().__init__(names, keyboard=keyboard, detail_help_text=detail_help_text)

    def start(self):
        if self.vk_event.args:
            command = find_command_by_name(self.vk_event.args[0].lower())
            if not command:
                return "Я не знаю такой команды"
            else:
                return get_help_for_command(command)
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
        if help_texts['games']:
            output += "\n\n— игры —\n"
            output += help_texts['games']

        return output
