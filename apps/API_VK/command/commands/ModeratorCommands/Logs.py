from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command._DoTheLinuxComand import do_the_linux_command


class Logs(CommonCommand):
    def __init__(self):
        names = ["лог", "логи"]
        help_text = "̲Л̲о̲г - логи веб-сервера"
        super().__init__(names, help_text, for_moderator=True, check_int_args=[0])

    def start(self):
        count = 50

        if self.vk_event.args:
            count = self.vk_event.args[0]

        command = "systemctl status xoma163site -n{}".format(count)
        try:
            output = do_the_linux_command(command)


            # Обрезаем инфу самого systemctl
            index_command = output.find(command)
            if index_command != -1:
                output = output[output.find(command) + len(command):]

            # Удаляем всё до старта
            start_string = "*** uWSGI is running in multiple interpreter mode ***"
            if output.find(start_string) != -1:
                output = output[output.find(start_string) + len(start_string):]

            # Удаляем везде вхождения этой ненужной строки
            index_removing = output.find("server uwsgi[")
            if index_removing != -1:
                for_removing = output[index_removing:output.find(']', index_removing + 1) + 1]
                output = output.replace(for_removing, '')

            output = "Логи:\n" + output + "\n"
            words = ["GET", "POST", "spawned uWSGI", "Not Found:"]
            for word in words:
                while output.find(word) != -1:
                    word_index = output.find(word)
                    left_index = output.rfind('\n', 0, word_index - len(word))
                    right_index = output.find('\n', word_index)
                    output = output[:left_index] + output[right_index:]

            return output
        except Exception as e:
            return "Ошибка:\n{}".format(str(e))
