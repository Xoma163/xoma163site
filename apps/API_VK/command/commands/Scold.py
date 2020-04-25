from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.commands.Praise import get_praise_or_scold


class Scold(CommonCommand):
    def __init__(self):
        names = ["обосрать", "обосри", "поругать", "поругай"]
        help_text = "Обосрать - рандомное оскорбление"
        detail_help_text = "Обосрать [кто-то] [род+число] - рандомное оскорбление\n" \
                           "Род и число указываются через последний аргумент: Мужской м, Женский ж, Средний с. Число: единственное *1, множественное *м\n" \
                           "Т.е. доступные сочетания аргументов могут быть следующими: [м ж с м1 ж1 с1 мм жм]\n" \
                           "Если в качестве параметра передаётся имя, фамилия, логин/id, никнейм, то род выберится из БД\n" \
                           "Пример. /обосрать бабушка ж"

        super().__init__(names, help_text, detail_help_text)

    def start(self):
        return get_praise_or_scold(self.vk_bot, self.vk_event, 'bad')
