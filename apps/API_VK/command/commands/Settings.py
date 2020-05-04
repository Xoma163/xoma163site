from apps.API_VK.command.CommonCommand import CommonCommand

phrase_translator = {
    'on': True,
    'вкл': True,
    '1': True,
    'true': True,
    'включить': True,
    'включи': True,
    'вруби': True,

    'off': False,
    'выкл': False,
    '0': False,
    'false': False,
    'выключить': False,
    'выключи': False,
    'выруби': False
}


class Settings(CommonCommand):
    def __init__(self):
        names = ["настройки", "настройка"]
        help_text = "Настройки - устанавливает некоторые настройки пользователя/чата"
        detail_help_text = "Настройки (настройка) (вкл/выкл) - устанавливает некоторые настройки пользователя/чата\n" \
                           "Настройки реагировать (вкл/выкл) - определяет, будет ли бот реагировать на неправильные команды. Это сделано для того, чтобы в конфе с несколькими ботами не было ложных срабатываний\n" \
                           ""
        super().__init__(names, help_text, detail_help_text, args=2)

    def start(self):

        if self.vk_event.args[1] in phrase_translator:
            value = phrase_translator[self.vk_event.args[1]]
        else:
            return "Не понял, включить или выключить?"

        if self.vk_event.args[0] in ['реагировать', 'реагируй', 'реагирование']:
            self.check_conversation()
            self.check_sender('conference_admin')
            self.vk_event.chat.need_reaction = value
            self.vk_event.chat.save()
            return "Сохранил настройку"
        else:
            return "Не знаю такой настройки"
