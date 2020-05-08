from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.Consts import Role
from apps.API_VK.command.DoTheLinuxComand import do_the_linux_command


def remove_rows_if_find_word(old_str, word):
    while old_str.find(word) != -1:
        word_index = old_str.find(word)
        left_index = old_str.rfind('\n', 0, word_index - len(word))
        right_index = old_str.find('\n', word_index)
        old_str = old_str[:left_index] + old_str[right_index:]
    return old_str


def get_server_logs(command):
    output = do_the_linux_command(command)

    # Обрезаем инфу самого systemctl
    index_command = output.find(command)
    if index_command != -1:
        output = output[index_command + len(command) + 1:]
    else:
        start_command = "/var/www/xoma163.site/venv/bin/uwsgi --ini /var/www/xoma163.site/uWSGI_nginx/uwsgi.ini"
        index_command = output.rfind(start_command)
        if index_command != -1:
            output = output[index_command + len(start_command) + 1:]

    # Удаляем всё до старта
    start_string = "*** uWSGI is running in multiple interpreter mode ***"
    if output.find(start_string) != -1:
        output = output[output.find(start_string) + len(start_string):]

    # Удаляем везде вхождения этой ненужной строки
    index_removing = output.find("server python[")
    if index_removing != -1:
        for_removing = output[index_removing:output.find(']', index_removing + 1) + 1]
        output = output.replace(for_removing, '')

    output = "Логи:\n" + output + "\n"
    words = ["GET", "POST", "spawned uWSGI", "Not Found:", "HEAD", "pidfile", "WSGI app 0", "Bad Request",
             "HTTP_HOST", "OPTIONS "]
    for word in words:
        output = remove_rows_if_find_word(output, word)
    return output


def get_bot_logs(command):
    output = do_the_linux_command(command)

    # Обрезаем инфу самого systemctl
    index_command = output.find(command)
    if index_command != -1:
        output = output[index_command + len(command) + 1:]

    index_removing = output.find("server python[")
    if index_removing != -1:
        for_removing = output[index_removing:output.find(']', index_removing + 1) + 1]
        output = output.replace(for_removing, '')
    words = ["USER=root", "user root", "Stopped", "Started"]
    for word in words:
        output = remove_rows_if_find_word(output, word)
    output = "Логи:\n" + output + "\n"
    return output


class Logs(CommonCommand):
    def __init__(self):
        names = ["логи", "лог"]
        help_text = "Логи - логи бота или сервера"
        detail_help_text = "Логи [сервис=бот] [кол-во строк=50] - логи. \n" \
                           "Сервис - бот или сервер"
        keyboard = {'for': Role.MODERATOR.name, 'text': 'Логи', 'color': 'blue', 'row': 1, 'col': 1}
        super().__init__(names, help_text, detail_help_text, access=Role.MODERATOR.name, keyboard=keyboard)

    def start(self):
        count = 50

        if self.vk_event.args:
            try:
                count = int(self.vk_event.args[-1])
                del self.vk_event.args[-1]
            except ValueError:
                pass

        if self.vk_event.args:
            if self.vk_event.args[0] in ['веб', 'web', 'сайт', 'site']:
                command = f"systemctl status xoma163site -n{count}"
                return get_server_logs(command)
            elif self.vk_event.args[0] in ['бот', 'bot']:
                command = f"systemctl status xoma163bot -n{count}"
                return get_bot_logs(command)
            else:
                return 'Нет такого модуля'

        command = f"systemctl status xoma163bot -n{count}"
        return get_bot_logs(command)
