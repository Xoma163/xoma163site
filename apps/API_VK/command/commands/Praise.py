from apps.API_VK.command.CommonCommand import CommonCommand, get_random_item_from_list
from apps.API_VK.static_texts import get_praises


class Praise(CommonCommand):
    def __init__(self):
        names = ["похвалить", "похвали", "хвалить"]
        super().__init__(names)

    def start(self):
        if self.vk_event.args:
            if self.vk_event.args[0].lower() == "петрович":
                msg = "спс))"
            else:
                msg = get_random_item_from_list(get_praises(), self.vk_event.args[0])
        else:
            msg = get_random_item_from_list(get_praises())
        self.vk_bot.send_message(self.vk_event.chat_id, msg)
