from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command._DoTheLinuxComand import do_the_linux_command
from apps.Statistics.models import Service
from xoma163site.wsgi import cameraHandler


class Stop(CommonCommand):
    def __init__(self):
        names = ["стоп", "stop"]
        help_text = "̲С̲т̲о̲п - останавливает работу Петровича. " \
                    "С параметром можно отключить нужный модуль (синички, майн(1.12 1.15.1))"
        keyboard = [{'for': 'admin', 'text': 'Стоп', 'color': 'red', 'row': 1, 'col': 2},
                    {'for': 'admin', 'text': 'Стоп синички', 'color': 'red', 'row': 1, 'col': 4}]

        super().__init__(names, help_text, keyboard=keyboard)

    def start(self):
        if self.vk_event.args:
            if self.vk_event.args[0] == "синички":
                self.check_sender('moderator')
                if cameraHandler.is_active():
                    cameraHandler.terminate()
                    return "Финишируем синичек"
                else:
                    return "Синички уже финишировали"
            elif self.vk_event.args[0] in ["майн", "майнкрафт", "mine", "minecraft"]:
                self.check_sender('minecraft')
                if len(self.vk_event.args) >= 2 and (
                        self.vk_event.args[1] == '1.12' or self.vk_event.args[1] == '1.12.2'):
                    self.check_command_time('minecraft_1.12', 90)

                    do_the_linux_command('sudo systemctl stop minecraft_1.12.2')
                    Service.objects.filter(name='stop_minecraft_1.12.2').delete()
                    return "Финишируем майн 1.12!"
                elif (len(self.vk_event.args) >= 2 and (
                        self.vk_event.args[1] == '1.15.1' or self.vk_event.args[1] == '1.15')) or len(
                        self.vk_event.args) == 1:
                    self.check_command_time('minecraft_1.15.1', 30)

                    do_the_linux_command('sudo systemctl stop minecraft_1.15.1')
                    Service.objects.filter(name='stop_minecraft_1.15.1').delete()
                    return "Финишируем майн 1.15.1!"
                else:
                    return "Я не знаю такой версии"
            elif self.vk_event.args[0] in ['террария', 'terraria']:
                self.check_sender('terraria')
                self.check_command_time('terraria', 10)
                do_the_linux_command('sudo systemctl stop terraria')
                return "Финишируем террарию!"
            else:
                return "Не найден такой модуль"
        else:
            self.check_sender('admin')
            self.vk_bot.BOT_CAN_WORK = False
            cameraHandler.terminate()
            return "Финишируем"
