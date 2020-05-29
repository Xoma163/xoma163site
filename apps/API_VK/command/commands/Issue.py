from apps.API_VK.command.CommonCommand import CommonCommand
from apps.service.models import Issue as IssueModel


class Issue(CommonCommand):
    def __init__(self):
        names = ["ишю", "ишью"]
        help_text = "Ишью - добавляет проблему Петровича, которую нужно решить"
        detail_help_text = "Ишью (текст/пересланные сообщения) - добавляет проблему Петровича, которую нужно решить"
        super().__init__(names, help_text, detail_help_text, api=False)

    def start(self):
        msgs = self.vk_event.fwd
        if not msgs:
            if not self.vk_event.original_args:
                return "Требуется аргументы или пересылаемые сообщения"

            msgs = [{'text': self.vk_event.original_args, 'from_id': int(self.vk_event.sender.user_id)}]
        issue_text = ""
        for msg in msgs:
            text = msg['text']
            if msg['from_id'] > 0:
                fwd_user_id = int(msg['from_id'])
                fwd_user = self.vk_bot.get_user_by_id(fwd_user_id)
                username = fwd_user.name + " " + fwd_user.surname
            else:
                fwd_user_id = int(msgs[0]['from_id'])
                username = self.vk_bot.get_bot_by_id(fwd_user_id).name
            issue_text += f"{username}:\n{text}\n\n"

        issue = IssueModel(
            author=self.vk_event.sender,
            text=issue_text)
        issue.save()
        return "Сохранено"
