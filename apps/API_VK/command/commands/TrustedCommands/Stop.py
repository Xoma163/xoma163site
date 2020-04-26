from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command._DoTheLinuxComand import do_the_linux_command
from apps.API_VK.models import VkUser
from apps.service.models import Service
from xoma163site.wsgi import cameraHandler


class Stop(CommonCommand):
    def __init__(self):
        names = ["стоп", "stop"]
        help_text = "Стоп - останавливает работу бота или модуля"
        detail_help_text = "Стоп [сервис=бот [версия=1.15.1]] - останавливает сервис\n" \
                           "Сервис - бот/синички/майнкрафт/террарию\n" \
                           "Если майнкрафт, то может быть указана версия, 1.12.2 или 1.15.1"

        keyboard = [{'for': 'admin', 'text': 'Стоп', 'color': 'red', 'row': 1, 'col': 2},
                    {'for': 'admin', 'text': 'Стоп синички', 'color': 'red', 'row': 1, 'col': 4}]
        super().__init__(names, help_text, detail_help_text, keyboard=keyboard, access='trusted')

    def start(self):
        if self.vk_event.args:
            if self.vk_event.args[0] == "синички":
                self.check_sender('admin')
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

                    message = "Финишируем майн 1.12!"
                    users_notify = VkUser.objects.filter(groups__name='minecraft_notify') \
                        .exclude(id=self.vk_event.sender.id)
                    users_chat_id_notify = [user.user_id for user in users_notify]
                    self.vk_bot.parse_and_send_msgs_thread(users_chat_id_notify,
                                                           message + f"\nИнициатор - {self.vk_event.sender}")

                    return message
                elif (len(self.vk_event.args) >= 2 and (
                        self.vk_event.args[1] == '1.15.1' or self.vk_event.args[1] == '1.15')) or len(
                    self.vk_event.args) == 1:
                    self.check_command_time('minecraft_1.15.1', 30)

                    do_the_linux_command('sudo systemctl stop minecraft_1.15.1')
                    Service.objects.filter(name='stop_minecraft_1.15.1').delete()

                    message = "Финишируем майн 1.15.1"
                    users_notify = VkUser.objects.filter(groups__name='minecraft_notify') \
                        .exclude(id=self.vk_event.sender.id)
                    users_chat_id_notify = [user.user_id for user in users_notify]
                    self.vk_bot.parse_and_send_msgs_thread(users_chat_id_notify,
                                                           message + f"\nИнициатор - {self.vk_event.sender}")

                    return message
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
            self.check_sender(['admin'])
            self.vk_bot.BOT_CAN_WORK = False
            cameraHandler.terminate()
            return "Финишируем"
