from apps.API_VK.APIs.Minecraft import MinecraftAPI, get_minecraft_version_by_args
from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.Consts import Role
from apps.API_VK.command.DoTheLinuxComand import do_the_linux_command
from apps.birds.CameraHandler import CameraHandler

cameraHandler = CameraHandler()


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
            minecraft_server = get_minecraft_version_by_args(self.vk_event.args)
            if not minecraft_server:
                return "Я не знаю такой версии"
            version = minecraft_server['names'][0]
            self.check_command_time(f'minecraft_{version}', minecraft_server['delay'])
            minecraft_api = MinecraftAPI(
                version,
                vk_bot=self.vk_bot,
                vk_event=self.vk_event,
                amazon=minecraft_server['amazon'])
            minecraft_api.start()

            message = f"Стартуем майн {version}"
            return message

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


