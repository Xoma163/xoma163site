import subprocess

from apps.API_VK.command.CommonCommand import CommonCommand


class Logs(CommonCommand):
    def __init__(self):
        names = ["лог", "логи"]
        help_text = "̲Л̲о̲г - логи веб-сервера"
        super().__init__(names, help_text, for_moderator=True)

    def start(self):
        count = 50

        if self.vk_event.args:
            try:
                count = int(self.vk_event.args[0])
            except Exception as e:
                self.vk_bot.send_message(self.vk_event.chat_id, "Аргумент должен быть целочисленным")
                return

        command = "systemctl status xoma163site -n{}".format(count)
        try:
            process = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE)
            output, error = process.communicate()
            output = output.decode("utf-8")

            # Обрезаем инфу самого systemctl
            output = output[output.find(command) + len(command):]

            # Удаляем всё до старта
            start_string = "*** uWSGI is running in multiple interpreter mode ***"
            if output.find(start_string):
                output = output[output.find(start_string) + len(start_string):]

            # Удаляем везде вхождения этой ненужной строки
            index_removing = output.find("server uwsgi[")
            for_removing = output[index_removing:output.find(']', index_removing + 1) + 1]
            output = output.replace(for_removing, '')

            if error:
                output += "\n{}".format(error)

            self.vk_bot.send_message(self.vk_event.chat_id, output)
        except Exception as e:
            self.vk_bot.send_message(self.vk_event.chat_id, "Ошибка:\n{}".format(str(e)))
