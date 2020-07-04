from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import localize_datetime, remove_tz
from apps.API_VK.command.Consts import Role
from apps.service.models import Notify


def get_notifies_from_object(notifies_obj, timezone, print_username=False):
    if len(notifies_obj) == 0:
        return "Нет напоминаний"
    result = ""

    for notify in notifies_obj:
        notify_datetime = localize_datetime(remove_tz(notify.date), timezone)

        if print_username:
            result += f"{notify.author}\n"
        if notify.repeat:
            result += f"{str(notify_datetime.strftime('%H:%M'))} - Постоянное"
        else:
            result += f"{str(notify_datetime.strftime('%d.%m.%Y %H:%M'))}"
        if notify.chat:
            result += f" (Конфа - {notify.chat.name})"
        result += f"\n{notify.text}\n\n"

    return result


class Notifies(CommonCommand):
    def __init__(self):
        names = ["напоминания", "оповещения"]
        help_text = "Напоминания - список напоминаний"
        detail_help_text = "Напоминания - список напоминаний. Отправляет в лс все напоминания, когда-либо созданные, в группу - только напоминания внутри группы\n" \
                           "Напоминания удалить (текст напоминания) - удаляет напоминания\n" \
                           "Напоминания конфа - выводит все напоминания по конфе\n" \
                           "Напоминания (имя, фамилия, логин/id, никнейм) - напоминания пользователя по конфе\n" \
                           "Админ конфы может удалять напоминания остальных участников"
        super().__init__(names, help_text, detail_help_text, api=False)

    def start(self):
        if self.vk_event.sender.city is None:
            return "Не знаю ваш город. /город"
        self.user_timezone = self.vk_event.sender.city.timezone.name

        if not self.vk_event.args:
            return self.menu_notifications()
        else:
            arg0 = self.vk_event.args[0].lower()

            menu = [
                [["удалить", "удали"], self.menu_delete],
                [["конфа", "беседе", "конфы", "беседы"], self.menu_conference],
                [['default'], self.menu_get_for_user],
            ]
            method = self.handle_menu(menu, arg0)
            return method()

    def menu_delete(self):
        self.check_args(2)
        notifies = Notify.objects.filter(author=self.vk_event.sender).order_by("date")
        if self.vk_event.chat:
            try:
                self.check_sender(Role.CONFERENCE_ADMIN)
                notifies = Notify.objects.filter(chat=self.vk_event.chat).order_by("date")
            except RuntimeError:
                notifies = notifies.filter(chat=self.vk_event.chat)
        filter_list = self.vk_event.args[1:]
        for _filter in filter_list:
            notifies = notifies.filter(text_for_filter__icontains=_filter)

        if len(notifies) == 0:
            return "Не нашёл напоминаний по такому тексту"
        if len(notifies) > 1:
            notifies10 = notifies[:10]
            notifies_texts = [str(notify.author) + " " + notify.text_for_filter for notify in notifies10]
            notifies_texts_str = "\n".join(notifies_texts)
            return f"Нашёл сразу несколько. Уточните:\n" \
                   f"{notifies_texts_str}"

        notifies.delete()
        return "Удалил"

    def menu_conference(self):
        self.check_conversation()
        notifies = Notify.objects.filter(chat=self.vk_event.chat)
        return get_notifies_from_object(notifies, self.user_timezone, True)

    def menu_get_for_user(self):
        self.check_conversation()
        user = self.vk_bot.get_user_by_name(self.vk_event.original_args, self.vk_event.chat)
        notifies = Notify.objects.filter(author=user, chat=self.vk_event.chat)
        return get_notifies_from_object(notifies, self.user_timezone, True)

    def menu_notifications(self):
        notifies = Notify.objects.filter(author=self.vk_event.sender).order_by("date")
        if self.vk_event.chat:
            notifies = notifies.filter(chat=self.vk_event.chat)
        return get_notifies_from_object(notifies, self.user_timezone)
