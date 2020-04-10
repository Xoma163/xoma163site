from apps.API_VK.command.CommonCommand import CommonCommand
from apps.service.models import Issue


class Issues(CommonCommand):
    def __init__(self):
        names = ["ишюс", "ишьюс", "иши"]
        help_text = "Ишьюс - список проблем"
        super().__init__(names, help_text)

    def start(self):
        issues = Issue.objects.all()
        features_text = "Добавленные ишю:\n\n"
        for i, feature in enumerate(issues):
            features_text += f"------------------------------{i + 1}------------------------------\n" \
                             f"{feature.text}\n"
        return features_text
