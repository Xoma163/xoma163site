import random

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import check_user_group, random_event
from apps.API_VK.static_texts import get_bad_words, get_bad_answers


class YesNo(CommonCommand):
    def __init__(self):
        names = ["вопрос", "?"]
        help_text = "...? - вернёт да или нет"
        detail_help_text = "...? - вернёт да или нет. Для вызова команды просто в конце нужно написать знак вопроса"
        super().__init__(names, help_text, detail_help_text, priority=50)

    def accept(self, vk_event):
        if (vk_event.msg and vk_event.msg[-1] == '?') or vk_event.command in self.names:
            return True
        return False

    def start(self):
        bad_words = get_bad_words()

        if not check_user_group(self.vk_event.sender, 'admin'):
            min_index_bad = len(self.vk_event.msg)
            max_index_bad = -1
            for word in bad_words:
                ind = self.vk_event.msg.lower().find(word)
                if ind != -1:
                    if ind < min_index_bad:
                        min_index_bad = ind
                    if ind > max_index_bad:
                        max_index_bad = ind

            min_index_bad = self.vk_event.msg.rfind(' ', 0, min_index_bad)
            if min_index_bad == -1:
                min_index_bad = self.vk_event.msg.rfind(',', 0, min_index_bad)
                if min_index_bad == -1:
                    min_index_bad = self.vk_event.msg.rfind('.', 0, min_index_bad)
                    if min_index_bad == -1:
                        min_index_bad = self.vk_event.msg.find('/')
            min_index_bad += 1
            if max_index_bad != -1:
                len_bad = self.vk_event.msg.find(',', max_index_bad)
                if len_bad == -1:
                    len_bad = self.vk_event.msg.find(' ', max_index_bad)
                    if len_bad == -1:
                        len_bad = self.vk_event.msg.find('?', max_index_bad)
                        if len_bad == -1:
                            len_bad = len(self.vk_event.msg)

                bad_answers = get_bad_answers()
                rand_int = random.randint(0, len(bad_answers) - 1)
                messages = [bad_answers[rand_int]]
                name = self.vk_event.sender.name
                if self.vk_event.sender.gender == '1':
                    msg_self = "сама"
                else:
                    msg_self = "сам"
                messages.append(f"{name}, может ты {msg_self} {self.vk_event.msg[min_index_bad: len_bad]}?")
                return messages

        random_events = [["Да", "Ага", "Канеш", "Само собой", "Абсолютно"],
                         ["Нет", "Неа", "Ни за что", "Невозможно", "NO"],
                         ["Ну тут даже я хз", "ДА НЕ ЗНАЮ Я", "Хз", "Спроси у другого бота", "Да нет наверное"]]
        probability_events1 = [48, 48, 4]
        probability_events2 = [80, 5, 5, 5, 5]
        selected_event = random_event(random_events, probability_events1)
        selected_event2 = random_event(selected_event, probability_events2)
        return selected_event2
