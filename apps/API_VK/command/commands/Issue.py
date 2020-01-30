from apps.API_VK.command.CommonCommand import CommonCommand
from apps.Statistics.views import append_feature


class Issue(CommonCommand):
    def __init__(self):
        names = ["ишю", "ишью"]
        help_text = "Ишью - добавляет проблему Петровича, которую нужно решить"
        detail_help_text = "Ишью ([N]), либо пересылаемые сообщения - добавляет проблему Петровича, которую нужно решить. Для работы требуется либо пересылаемое сообщение, либо аргумент"
        super().__init__(names, help_text, detail_help_text, api=False)

    def start(self):
        msgs = self.vk_event.fwd
        if not msgs:
            if not self.vk_event.original_args:
                return "Требуется аргументы или пересылаемые сообщения"

            msgs = [{'text': self.vk_event.original_args, 'from_id': int(self.vk_event.sender.user_id)}]
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
            feature_text += f"{username}:\n{text}\n\n"
        append_feature(feature_text)
        return "Сохранено"
