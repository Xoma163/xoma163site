from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.Consts import Role
from apps.service.models import Issue


class DeIssue(CommonCommand):
    def __init__(self):
        names = ["деишю", "деишью", "хуишю", "хуишью"]
        help_text = "Хуишью - удаляет последнюю добавленную проблему"
        super().__init__(names, help_text, api=False, access=Role.ADMIN)

    def start(self):
        issue = Issue.objects.last()
        issue_text = issue.text
        issue.delete()
        return f'Ишю удалено:\n{issue_text}'
