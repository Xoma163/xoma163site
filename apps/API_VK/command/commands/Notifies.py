from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import localize_datetime, remove_tz
from apps.service.models import Notify


class Notifies(CommonCommand):
    def __init__(self):
        names = ["напоминания", "оповещения"]
        help_text = "Напоминания - список напоминаний"
        super().__init__(names, help_text)

    def start(self):
        notifies = Notify.objects.filter(author=self.vk_event.sender)
        if len(notifies) == 0:
            return "Нет напоминаний"
        result = ""

        user_timezone = self.vk_event.sender.city.timezone
        for notify in notifies:
            notify_datetime = localize_datetime(remove_tz(notify.date), user_timezone)

            result += f"{str(notify_datetime.strftime('%d.%m.%Y %H:%M'))}\n" \
                      f"{notify.text}\n\n"

        return result
