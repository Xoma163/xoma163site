from apps.API_VK.command import Role
from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import check_user_group, find_command_by_name, get_help_for_command


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
        output = "— общие команды —\n"
        output += help_texts[Role.USER.name]

        if check_user_group(self.vk_event.sender, Role.TERRARIA.name) and help_texts[Role.TERRARIA.name]:
            output += "\n\n— команды для группы 6221 —\n"
            output += help_texts[Role.TERRARIA.name]
        if check_user_group(self.vk_event.sender, Role.MODERATOR.name) and help_texts[Role.MODERATOR.name]:
            output += "\n\n— команды для модераторов —\n"
            output += help_texts[Role.MODERATOR.name]
        if check_user_group(self.vk_event.sender, Role.ADMIN.name) and help_texts[Role.ADMIN.name]:
            output += "\n\n— команды для администраторов —\n"
            output += help_texts[Role.ADMIN.name]
        if check_user_group(self.vk_event.sender, Role.BANNED.name) and help_texts[Role.BANNED.name]:
            output += "\n\n— команды для забаненных —\n"
            output += help_texts[Role.BANNED.name]
        if check_user_group(self.vk_event.sender, Role.MINECRAFT.name) and help_texts[Role.MINECRAFT.name]:
            output += "\n\n— команды для игроков майнкрафта —\n"
            output += help_texts[Role.MINECRAFT.name]
        if check_user_group(self.vk_event.sender, Role.MINECRAFT_NOTIFY.name) and help_texts[
            Role.MINECRAFT_NOTIFY.name]:
            output += "\n\n— команды для уведомлённых майнкрафтеров —\n"
            output += help_texts[Role.MINECRAFT_NOTIFY.name]
        if check_user_group(self.vk_event.sender, Role.TERRARIA.name) and help_texts[Role.TERRARIA.name]:
            output += "\n\n— команды для игроков террарии —\n"
            output += help_texts[Role.TERRARIA.name]
        if check_user_group(self.vk_event.sender, Role.TRUSTED.name) and help_texts[Role.TRUSTED.name]:
            output += "\n\n— команды для доверенных пользователей —\n"
            output += help_texts[Role.TRUSTED.name]
        if help_texts['games']:
            output += "\n\n— игры —\n"
            output += help_texts['games']

        return output
