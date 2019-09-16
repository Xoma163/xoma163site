import datetime
import threading

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id

from apps.API_VK.models import Log
from xoma163site.settings import BASE_DIR


# ToDo: Логгирование в txt ещё
class VkBot(threading.Thread):

    def send_message(self, id, msg):
        self.vk.messages.send(peer_id=id,
                              message=msg,
                              access_token=self._TOKEN,
                              random_id=get_random_id()
                              )

    def message_to_me(self, msg):
        return msg.find(self.mention) >= 0

    def parse_msg(self, msg):
        return msg.replace(self.mention + ' ', '') \
            .replace(self.mention + ', ', '') \
            .replace(self.mention + ',', '') \
            .replace('\r', '').replace('\n', '') \
            .lower()

    def __init__(self):
        super().__init__()
        f = open(BASE_DIR + "/secrets/vk.txt", "r")
        self._TOKEN = f.readline().replace('\r', '').replace('\n', '')
        group_id = int(f.readline().replace('\r', '').replace('\n', ''))
        vk_session = vk_api.VkApi(token=self._TOKEN)
        self.longpoll = MyVkBotLongPoll(vk_session, group_id=group_id)
        self.vk = vk_session.get_api()
        self.mention = f.readline().replace('\r', '').replace('\n', '')
        f.close()

    def listen_longpoll(self):
        for event in self.longpoll.listen():
            try:
                # Если пришло новое сообщение
                if event.type == VkBotEventType.MESSAGE_NEW:
                    message = event.object.text
                    if self.message_to_me(message):
                        message = self.parse_msg(message)
                        if message == "привет":
                            self.send_message(event.object.peer_id, "Хай")
                        elif message == "пока":
                            self.send_message(event.object.peer_id, "Пока((")
                        elif message == "синички":
                            self.send_message(event.object.peer_id, "http://birds.xoma163.site")
                        elif message == "где андрей" or message == "где андрей?":
                            today = datetime.datetime.now()
                            # ToDo: сделать только для нужного юзера (Андрей)
                            vk_event = Log.objects.filter(success=True,
                                                          date__year=today.year,
                                                          date__month=today.month,
                                                          date__day=today.day).last()
                            if vk_event is None:
                                msg = "Информации пока ещё нет"
                            else:
                                msg = "%s\n%s" % (vk_event.date.strftime("%H:%M:%S"), vk_event.msg)
                            self.send_message(event.object.peer_id, str(msg))
                        else:
                            self.send_message(event.object.peer_id, "Игорь Петрович не понял команды " + message)
            except Exception as e:
                print('ОШИБКА ВЫПОЛНЕНИЯ ЛОНГПОЛА 1:', e)

    def run(self):
        self.listen_longpoll()


class MyVkBotLongPoll(VkBotLongPoll):
    def listen(self):
        while True:
            try:
                for event in self.check():
                    yield event
            except Exception as e:
                print('ОШИБКА ВЫПОЛНЕНИЯ ЛОНГПОЛА 2:', e)
