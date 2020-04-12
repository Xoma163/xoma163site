from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import localize_datetime, remove_tz
from apps.service.models import Notify


class Notifies(CommonCommand):
    def __init__(self):
        names = ["напоминания", "оповещения"]
        help_text = "Напоминания - список напоминаний"
        detail_help_text = "Напоминания - список напоминаний. Отправляет в лс все напоминания, когда либо созданные, в группу - только напоминания внутри группы\n" \
                           "Напоминания удалить ({текст напоминания}) - удаляет напоминания"
        super().__init__(names, help_text, detail_help_text)

    def start(self):
        if self.vk_event.args:
            if self.vk_event.args[0].lower() in ["удалить", "удали"]:
                notifies = Notify.objects.filter(author=self.vk_event.sender)
                if self.vk_event.from_chat:
                    notifies.filter(chat=self.vk_event.chat)
                filter_list = self.vk_event.args[1:]
                for _filter in filter_list:
                    notifies = notifies.filter(text_for_filter__icontains=_filter)

                if len(notifies) == 0:
                    return "Не нашёл напоминаний по такому тексту"
                if len(notifies) > 1:
                    notifies10 = notifies[:10]
                    notifies_texts = [notify.text_for_filter for notify in notifies10]
                    notifies_texts_str = "\n".join(notifies_texts)
                    return f"Нашёл сразу несколько. Уточните:\n" \
                           f"{notifies_texts_str}"

                notifies.delete()
                return "Удалил"
            else:
                return "Доступные команды - [удалить]"
        else:
            notifies = Notify.objects.filter(author=self.vk_event.sender)
            if self.vk_event.from_chat:
                notifies.filter(chat=self.vk_event.chat)
            if len(notifies) == 0:
                return "Нет напоминаний"
            result = ""

            user_timezone = self.vk_event.sender.city.timezone
            for notify in notifies:
                notify_datetime = localize_datetime(remove_tz(notify.date), user_timezone)

                if notify.repeat:
                    result += f"{str(notify_datetime.strftime('%H:%M'))} - Постоянное"
                else:
                    result += f"{str(notify_datetime.strftime('%d.%m.%Y %H:%M'))}"
                if notify.from_chat:
                    result += f" (Конфа - {notify.chat.name})"
                result += f"\n{notify.text}\n\n"

            return result
