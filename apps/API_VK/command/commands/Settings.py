from django.contrib.auth.models import Group

from apps.API_VK.command import Role
from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.Consts import on_off_translator


class Settings(CommonCommand):
    def __init__(self):
        names = ["настройки", "настройка"]
        help_text = "Настройки - устанавливает некоторые настройки пользователя/чата"
        detail_help_text = "Настройки (настройка) (вкл/выкл) - устанавливает некоторые настройки пользователя/чата\n" \
                           "Настройки реагировать (вкл/выкл) - определяет, будет ли бот реагировать на неправильные команды. " \
                           "Это сделано для того, чтобы в конфе с несколькими ботами не было ложных срабатываний\n\n" \
                           "Для доверенных:\n" \
                           "Настройки реагировать (вкл/выкл) - определяет, будет ли бот присылать информацию о сервере майна."
        super().__init__(names, help_text, detail_help_text, args=2)

    def start(self):

        if self.vk_event.args[1] in on_off_translator:
            value = on_off_translator[self.vk_event.args[1]]
        else:
            return "Не понял, включить или выключить?"

        if self.vk_event.args[0] in ['реагировать', 'реагируй', 'реагирование']:
            self.check_conversation()
            self.check_sender(Role.CONFERENCE_ADMIN.name)
            self.vk_event.chat.need_reaction = value
            self.vk_event.chat.save()
            return "Сохранил настройку"
        if self.vk_event.args[0] in ['майнкрафт', 'майн', 'minecraft', 'mine']:
            self.check_sender(Role.TRUSTED.name)

            group_minecraft_notify = Group.objects.get(name=Role.MINECRAFT_NOTIFY.name)
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
