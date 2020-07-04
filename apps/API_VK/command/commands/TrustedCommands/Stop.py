from apps.API_VK.APIs.Minecraft import MinecraftAPI, get_minecraft_version_by_args
from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.Consts import Role
from apps.API_VK.command.DoTheLinuxComand import do_the_linux_command
from apps.birds.CameraHandler import CameraHandler

cameraHandler = CameraHandler()


class Stop(CommonCommand):
    def __init__(self):
        names = ["стоп", "stop"]
        help_text = "Стоп - останавливает работу бота или модуля"
        detail_help_text = "Стоп [сервис=бот [версия=1.15.1]] - останавливает сервис\n" \
                           "Сервис - бот/синички/майнкрафт/террария\n" \
                           "Если майнкрафт, то может быть указана версия, 1.12.2 или 1.15.1"

        keyboard = [{'for': Role.ADMIN, 'text': 'Стоп', 'color': 'red', 'row': 1, 'col': 2},
                    {'for': Role.ADMIN, 'text': 'Стоп синички', 'color': 'red', 'row': 1, 'col': 4}]
        super().__init__(names, help_text, detail_help_text, keyboard=keyboard, access=Role.TRUSTED)

    def start(self):
        if self.vk_event.args:
            arg0 = self.vk_event.args[0].lower()
        else:
            arg0 = None

        menu = [
            [["синички"], self.menu_birds],
            [["майн", "майнкрафт", "mine", "minecraft"], self.menu_minecraft],
            [['террария', 'terraria'], self.menu_terraria],
            [['бот', 'bot'], self.menu_bot],
            [['default'], self.menu_bot]
        ]
        method = self.handle_menu(menu, arg0)
        return method()

    def menu_birds(self):
        self.check_sender(Role.ADMIN)
        if cameraHandler.is_active():
            cameraHandler.terminate()
            return "Финишируем синичек"
        else:
            return "Синички уже финишировали"

    def menu_minecraft(self):
        self.check_sender(Role.MINECRAFT)
        version = None
        if len(self.vk_event.args) > 1:
            version = self.vk_event.args[1]
        minecraft_server = get_minecraft_version_by_args(version)
        if not minecraft_server:
            return "Я не знаю такой версии"
        version = minecraft_server['names'][0]
        self.check_command_time(f'minecraft_{version}', minecraft_server['delay'])
        minecraft_api = MinecraftAPI(
            version,
            vk_bot=self.vk_bot,
            vk_event=self.vk_event,
            amazon=minecraft_server['amazon'])
        minecraft_api.stop()

        message = f"Финишируем майн {version}"
        return message

    def menu_terraria(self):
        self.check_sender(Role.TERRARIA)
        self.check_command_time('terraria', 10)
        do_the_linux_command('sudo systemctl stop terraria')
        return "Финишируем террарию!"

    def menu_bot(self):
        self.check_sender(Role.ADMIN)
        self.vk_bot.BOT_CAN_WORK = False
        cameraHandler.terminate()
        return "Финишируем"
