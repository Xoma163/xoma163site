from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import check_user_group, find_command_by_name, get_help_for_command
from apps.API_VK.command.Consts import Role


class Help(CommonCommand):
    def __init__(self):
        names = ["помощь", "хелп", "ман", "команды", "помоги", "памаги", "спаси", "хелб", "манул", "help"]
        detail_help_text = "Формат детальной помощи по командам:\n" \
                           "Команда - выполняет команду\n" \
                           "Команда параметр - выполняет команду с параметром\n" \
                           "Команда (аргумент) - выполняет команду с обязательным аргументом\n" \
                           "Команда [аргумент=10] - выполняет команду с необязательным аргументов. Если не указать " \
                           "его, будет подставлено значение по умолчанию\n\n" \
                           "Формальный вид команды:\n" \
                           "Команда параметр (аргумент) [необязательный аргумент 1 [необязательный аргумент 2 при " \
                           "условии передачи первого аргумента]] [необязательный аргумент 3 со значением по умолчанию 20=20]"

        keyboard = {'text': 'Помощь', 'color': 'blue', 'row': 1, 'col': 2}
        super().__init__(names, keyboard=keyboard, detail_help_text=detail_help_text)

    def accept(self, vk_event):
        if vk_event.command in self.names:
            return True
        # Самая первая кнопка клавы у бота
        if vk_event.payload and vk_event.payload['command'] == 'start':
            return True
        return False

    def start(self):
        if self.vk_event.args:
            command = find_command_by_name(self.vk_event.args[0].lower())
            if not command:
                return "Я не знаю такой команды"
            else:
                self.check_sender(command.access)
                return get_help_for_command(command)
        from apps.API_VK.command import HELP_TEXT, API_HELP_TEXT

        if self.vk_event.from_api:
            help_texts = API_HELP_TEXT
        else:
            help_texts = HELP_TEXT

        ordered_roles = [
            {"role": Role.USER.name, "text": "общие команды"},
            {"role": Role.ADMIN.name, "text": "команды для администраторов"},
            {"role": Role.MODERATOR.name, "text": "команды для модераторов"},
            {"role": Role.MINECRAFT.name, "text": "команды для игроков майнкрафта"},
            {"role": Role.TRUSTED.name, "text": "команды для доверенных пользователей"},
            {"role": Role.STUDENT.name, "text": "команды для группы 6221"},
            {"role": Role.MINECRAFT_NOTIFY.name, "text": "команды для уведомлённых майнкрафтеров"},
            {"role": Role.TERRARIA.name, "text": "команды для игроков террарии"},
        ]
        output = ""
        for role in ordered_roles:
            if check_user_group(self.vk_event.sender, role['role']) and help_texts[role['role']]:
                output += f"\n\n— {role['text']} —\n"
                output += help_texts[role['role']]
        if help_texts['games']:
            output += "\n\n— игры —\n"
            output += help_texts['games']
        output = output.rstrip()
        return output
