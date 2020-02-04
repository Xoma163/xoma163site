import subprocess

from apps.API_VK.command.CommonCommand import CommonCommand


class Command(CommonCommand):
    def __init__(self):
        names = ["команда"]
        help_text = "Команда - запускает любую команду на сервере"
        detail_help_text = "Команда (N) - запускает любую команду на сервере с уровнем прав server, N - команда"
        super().__init__(names, help_text, detail_help_text, access='admin', args=1)

    def start(self):
        try:
            command = self.vk_event.params.split(' ')
            process = subprocess.Popen(command, stdout=subprocess.PIPE)
            output, error = process.communicate()
            output = output.decode("utf-8")
            if error:
                output += f"\n{error}"
            return output
        except Exception as e:
            return f"Ошибка:\n{str(e)}"
