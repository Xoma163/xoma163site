import random

from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.static_texts import get_bad_words, get_bad_answers


class YesNo(CommonCommand):
    def __init__(self):
        names = ["get_user_by_id"]
        help_text = "̲.̲.̲.̲? - вернёт да или нет."
        super().__init__(names)

    def accept(self, vk_bot, vk_event):
        self.vk_bot = vk_bot
        self.vk_event = vk_event

        if self.vk_event.full_message[-1] != '?':
            return False

        self.checks()
        self.start()
        return True

    def start(self):
        bad_words = get_bad_words()

        if not self.vk_event.sender.is_admin:
            min_index_bad = len(self.vk_event.full_message)
            max_index_bad = -1
            for word in bad_words:
                ind = self.vk_event.full_message.lower().find(word)
                if ind != -1:
                    if ind < min_index_bad:
                        min_index_bad = ind
                    if ind > max_index_bad:
                        max_index_bad = ind

            min_index_bad = self.vk_event.full_message.rfind(' ', 0, min_index_bad)
            if min_index_bad == -1:
                min_index_bad = self.vk_event.full_message.rfind(',', 0, min_index_bad)
                if min_index_bad == -1:
                    min_index_bad = self.vk_event.full_message.rfind('.', 0, min_index_bad)
                    if min_index_bad == -1:
                        min_index_bad = self.vk_event.full_message.find('/')
            min_index_bad += 1

            if max_index_bad != -1:
                len_bad = self.vk_event.full_message.find(',', max_index_bad)
                if len_bad == -1:
                    len_bad = self.vk_event.full_message.find(' ', max_index_bad)
                    if len_bad == -1:
                        len_bad = self.vk_event.full_message.find('?', max_index_bad)

                bad_answers = get_bad_answers()
                rand_int = random.randint(0, len(bad_answers) - 1)
                self.vk_bot.send_message(self.vk_event.chat_id, bad_answers[rand_int])
                name = self.vk_event.sender.name
                if self.vk_event.sender.gender == 1:
                    msg_self = "сама"
                else:
                    msg_self = "сам"
                msg = "{}, {} {} {}?".format(name, "может ты", msg_self,
                                             self.vk_event.full_message[min_index_bad: len_bad])
                self.vk_bot.send_message(self.vk_event.chat_id, msg)
                return

        rand_int = random.randint(1, 100)
        if rand_int <= 48:
            msg = "Да"
        elif rand_int <= 96:
            msg = "Нет"
        else:
            msg = "Ну тут даже я хз"
        self.vk_bot.send_message(self.vk_event.chat_id, msg)
        return
