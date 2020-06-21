from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import get_help_for_command, find_command_by_name


class Help(CommonCommand):
    def __init__(self):
        names = ["помощь", "хелп", "ман", "команды", "помоги", "памаги", "спаси", "хелб", "манул", "help"]
        help_text = "Помощь - помощь по командам и боту"
        super().__init__(names, help_text)

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
        text = "/помощь (название команды) - помощь по конкретной команде\n" \
               "/документация - документация по боту. Самый подробный мануал по всему в одном месте\n" \
               "/команды - список всех команд с кратким описанием\n" \
               "\n" \
               "Основы основ:\n" \
               "Пример конкретной команды: /рандом 10\n" \
               "* / — упоминание бота\n" \
               "* рандом — команда\n" \
               "* 10 — аргумент команды\n" \
               "\n" \
               "Формат детальной помощи по командам:\n" \
               "Команда - выполняет команду\n" \
               "Команда параметр - выполняет команду с параметром\n" \
               "Команда (аргумент) - выполняет команду с обязательным аргументом\n" \
               "Команда [аргумент=10] - выполняет команду с необязательным аргументом. Если не указать его, будет " \
               "подставлено значение по умолчанию"
        return text
