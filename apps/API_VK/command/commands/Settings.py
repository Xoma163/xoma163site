from django.contrib.auth.models import Group

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import check_user_group
from apps.API_VK.command.Consts import ON_OFF_TRANSLATOR, TRUE_FALSE_TRANSLATOR
from apps.API_VK.command.Consts import Role


class Settings(CommonCommand):
    def __init__(self):
        names = ["настройки", "настройка"]
        help_text = "Настройки - устанавливает некоторые настройки пользователя/чата"
        detail_help_text = "Настройки (настройка) (вкл/выкл) - устанавливает некоторые настройки пользователя/чата\n" \
                           "Настройки реагировать (вкл/выкл) - определяет, будет ли бот реагировать на неправильные команды. " \
                           "Это сделано для того, чтобы в конфе с несколькими ботами не было ложных срабатываний\n\n" \
                           "Для доверенных:\n" \
                           "Настройки реагировать (вкл/выкл) - определяет, будет ли бот присылать информацию о сервере майна."
        super().__init__(names, help_text, detail_help_text)

    def start(self):
        if self.vk_event.args:
            self.check_args(2)
            if self.vk_event.args[1].lower() in ON_OFF_TRANSLATOR:
                value = ON_OFF_TRANSLATOR[self.vk_event.args[1]]
            else:
                return "Не понял, включить или выключить?"
            arg0 = self.vk_event.args[0].lower()
            if arg0 in ['реагировать', 'реагируй', 'реагирование']:
                self.check_conversation()
                self.check_sender(Role.CONFERENCE_ADMIN)
                self.vk_event.chat.need_reaction = value
                self.vk_event.chat.save()
                return "Сохранил настройку"
            if arg0 in ['майнкрафт', 'майн', 'minecraft', 'mine']:
                self.check_sender(Role.TRUSTED)

                group_minecraft_notify = Group.objects.get(name=Role.MINECRAFT_NOTIFY)
                if value:
                    self.vk_event.sender.groups.add(group_minecraft_notify)
                    self.vk_event.sender.save()
                    return "Подписал на рассылку о сервере майна"
                else:
                    self.vk_event.sender.groups.remove(group_minecraft_notify)
                    self.vk_event.sender.save()
                    return "Отписал от рассылки о сервере майна"
            else:
                return "Не знаю такой настройки"
        else:
            msg = "Настройки:\n"
            if self.vk_event.chat:
                reaction = self.vk_event.chat.need_reaction
                msg += f"Реагировать на неправильные команды - {TRUE_FALSE_TRANSLATOR[reaction]}\n"

            if check_user_group(self.vk_event.sender, Role.TRUSTED):
                minecraft_notify = check_user_group(self.vk_event.sender, Role.MINECRAFT_NOTIFY)
                msg += f"Уведомления по майну - {TRUE_FALSE_TRANSLATOR[minecraft_notify]}\n"
            return msg
