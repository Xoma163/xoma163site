from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.Consts import Role
from apps.service.models import Issue


class DeIssue(CommonCommand):
    def __init__(self):
        names = ["деишю", "деишью", "хуишю", "хуишью"]
        help_text = "Ишью - добавляет проблему Петровича, которую нужно решить"
        detail_help_text = "Ишью (текст/пересланные сообщения) - добавляет проблему Петровича, которую нужно решить"
        super().__init__(names, help_text, detail_help_text, api=False, access=Role.ADMIN.name)

    def start(self):
        issue = Issue.objects.last()
        issue_text = issue.text
        issue.delete()
        return f'Ишю удалено:\n{issue_text}'
