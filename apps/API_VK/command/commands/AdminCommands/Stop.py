from apps.API_VK.command.CommonCommand import CommonCommand
from xoma163site.wsgi import cameraHandler


class Stop(CommonCommand):
    def __init__(self):
        names = ["стоп"]
        help_text = "̲С̲т̲о̲п - останавливает работу Петровича. С параметром можно отключить нужный модуль (синички)"
        super().__init__(names, help_text, for_admin=True)

    def start(self):
        if self.vk_event.args:
            if self.vk_event.args[0] == "синички":
                if cameraHandler.is_active():
                    cameraHandler.terminate()
                    self.vk_bot.send_message(self.vk_event.chat_id, "Финишируем синичек")
                else:
                    self.vk_bot.send_message(self.vk_event.chat_id, "Синички уже финишировали")
                return
        else:
            self.vk_bot.BOT_CAN_WORK = False
            self.vk_bot.send_message(self.vk_event.chat_id, "Финишируем")
