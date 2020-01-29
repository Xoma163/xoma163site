from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command._DoTheLinuxComand import do_the_linux_command


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
             "HTTP_HOST"]
    for word in words:
        while output.find(word) != -1:
            word_index = output.find(word)
            left_index = output.rfind('\n', 0, word_index - len(word))
            right_index = output.find('\n', word_index)
            output = output[:left_index] + output[right_index:]
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
    output = "Логи:\n" + output + "\n"
    return output


class Logs(CommonCommand):
    def __init__(self):
        names = ["лог", "логи", "logs", "log"]
        help_text = "Лог - логи"
        detail_help_text = "Лог ([N]) - логи. N - логи сервера или бота. Принимает ключ -n и количество строк в логах. Пример /лог сервер -n50"
        keyboard = {'for': 'moderator', 'text': 'Логи', 'color': 'blue', 'row': 1, 'col': 1}
        super().__init__(names, help_text, detail_help_text, access='moderator', keyboard=keyboard)

    def start(self):
        count = 50

        if self.vk_event.keys:
            if 'n' in self.vk_event.keys:
                count = self.vk_event.keys['n']

        if self.vk_event.args:
            if self.vk_event.args[0] in ['сервер', 'веб', 'server', 'web']:
                command = f"systemctl status xoma163site -n{count}"
                return get_server_logs(command)
            elif self.vk_event.args[0] in ['бот', 'bot']:
                command = f"systemctl status xoma163bot -n{count}"
                return get_bot_logs(command)
            else:
                return 'Нет такого модуля'
        else:
            command = f"systemctl status xoma163bot -n{count}"
            return get_bot_logs(command)
