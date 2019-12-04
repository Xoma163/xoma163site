from apps.API_VK.command.CommonCommand import CommonCommand
from apps.Statistics.views import append_feature


class Issue(CommonCommand):
    def __init__(self):
        names = ["ишю", "ишью"]
        help_text = "̲И̲ш̲ь̲ю + пересылаемые сообщения - добавлеет проблему Петровича, которую нужно решить"
        super().__init__(names, help_text)

    def start(self):
        msgs = self.vk_event.fwd
        if not msgs:
            msgs = [{'text': self.vk_event.original_args, 'from_id': self.vk_event.user_id}]
        feature_text = ""
        for msg in msgs:
            text = msg['text']
            if msg['from_id'] > 0:
                quote_user_id = int(msg['from_id'])
                quote_user = self.vk_bot.get_user_by_id(quote_user_id)
                username = quote_user.name + " " + quote_user.surname
            else:
                quote_user_id = int(msgs[0]['from_id']) * -1
                username = self.vk_bot.get_group_name_by_id(quote_user_id)
            feature_text += "{}:\n{}\n\n".format(username, text)
        append_feature(feature_text)
        self.vk_bot.send_message(self.vk_event.chat_id, "Сохранено")
