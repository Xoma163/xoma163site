from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.Consts import Role
from apps.API_VK.command.DoTheLinuxComand import do_the_linux_command
from apps.API_VK.models import VkUser
from xoma163site.wsgi import cameraHandler


class Start(CommonCommand):
    def __init__(self):
        names = ["старт", "start"]
        help_text = "Старт - возобновляет работу бота или модуля"
        detail_help_text = "Старт [сервис=бот [версия=1.15.1]] - стартует сервис\n" \
                           "Сервис - бот/синички/майнкрафт/террария\n" \
                           "Если майнкрафт, то может быть указана версия, 1.12.2 или 1.15.1"

        keyboard = [{'for': Role.ADMIN, 'text': 'Старт', 'color': 'green', 'row': 1, 'col': 1},
                    {'for': Role.ADMIN, 'text': 'Старт синички', 'color': 'green', 'row': 1, 'col': 3}]
        super().__init__(names, help_text, detail_help_text, keyboard=keyboard, access=Role.TRUSTED)

    def start(self):
        module = "bot"
        if self.vk_event.args:
            module = self.vk_event.args[0].lower()
        if module in ["синички"]:
            self.check_sender(Role.ADMIN)
            if not cameraHandler.is_active():
                cameraHandler.resume()
                return "Стартуем синичек!"
            else:
                return "Синички уже стартовали"
        elif module in ["майн", "майнкрафт", "mine", "minecraft"]:
            self.check_sender(Role.MINECRAFT)
            if len(self.vk_event.args) >= 2 and (
                    self.vk_event.args[1] == '1.12' or self.vk_event.args[1] == '1.12.2'):
                self.check_command_time('minecraft_1.12.2', 90)

                do_the_linux_command('sudo systemctl start minecraft_1.12.2')

                message = "Стартуем майн 1.12!"
                users_notify = VkUser.objects.filter(groups__name=Role.MINECRAFT_NOTIFY.name) \
                    .exclude(id=self.vk_event.sender.id)
                users_chat_id_notify = [user.user_id for user in users_notify]
                self.vk_bot.parse_and_send_msgs_thread(users_chat_id_notify,
                                                       message + f"\nИнициатор - {self.vk_event.sender}")

                return message
            elif (len(self.vk_event.args) >= 2 and (
                    self.vk_event.args[1] == '1.15.1' or self.vk_event.args[1] == '1.15')) or len(
                self.vk_event.args) == 1:
                self.check_command_time('minecraft_1.15.1', 30)

                do_the_linux_command('sudo systemctl start minecraft_1.15.1')

                message = "Стартуем майн 1.15.1"
                users_notify = VkUser.objects.filter(groups__name=Role.MINECRAFT_NOTIFY.name) \
                    .exclude(id=self.vk_event.sender.id)
                users_chat_id_notify = [user.user_id for user in users_notify]
                self.vk_bot.parse_and_send_msgs_thread(users_chat_id_notify,
                                                       message + f"\nИнициатор - {self.vk_event.sender}")
                return message
            else:
                return "Я не знаю такой версии"
        elif module in ['террария', 'terraria']:
            self.check_sender(Role.TERRARIA)
            self.check_command_time('terraria', 10)
            do_the_linux_command('sudo systemctl start terraria')
            return "Стартуем террарию!"
        elif module in ['бот', 'bot']:
            self.check_sender(Role.ADMIN)
            self.vk_bot.BOT_CAN_WORK = True
            cameraHandler.resume()
            return "Стартуем!"
        else:
            return "Не найден такой модуль"
