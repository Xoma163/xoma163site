from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import localize_datetime, remove_tz
from apps.service.models import Notify


class Notifies(CommonCommand):
    def __init__(self):
        names = ["напоминания", "оповещения"]
        help_text = "Напоминания - список напоминаний"
        detail_help_text = "Напоминания - список напоминаний. Отправляет в лс все напоминания, когда либо созданные, в группу - только напоминания внутри группы"
        super().__init__(names, help_text, detail_help_text)

    def start(self):
        if self.vk_event.from_chat:
            notifies = Notify.objects.filter(author=self.vk_event.sender, chat=self.vk_event.chat)
        else:
            notifies = Notify.objects.filter(author=self.vk_event.sender)
        if len(notifies) == 0:
            return "Нет напоминаний"
        result = ""

        user_timezone = self.vk_event.sender.city.timezone
        for notify in notifies:
            notify_datetime = localize_datetime(remove_tz(notify.date), user_timezone)

            result += f"{str(notify_datetime.strftime('%d.%m.%Y %H:%M'))}"
            if notify.from_chat:
                result += f" (Конфа - {notify.chat.name})"
            result += f"\n{notify.text}\n\n"

        return result
