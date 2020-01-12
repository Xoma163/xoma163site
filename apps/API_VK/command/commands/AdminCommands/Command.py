import subprocess

from apps.API_VK.command.CommonCommand import CommonCommand


class Command(CommonCommand):
    def __init__(self):
        names = ["команда"]
        help_text = "̲К̲о̲м̲а̲н̲д̲а - запускает любую команду на сервере"
        super().__init__(names, help_text, for_admin=True, need_args=1)

    def start(self):
        try:
            command = self.vk_event.original_args.split(' ')
            process = subprocess.Popen(command, stdout=subprocess.PIPE)
            output, error = process.communicate()
            output = output.decode("utf-8")
            if error:
                output += "\n{}".format(error)
            return output
        except Exception as e:
            return "Ошибка:\n{}".format(str(e))
