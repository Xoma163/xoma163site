import threading

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id

# from apps.API.models import Log
from xoma163site.settings import BASE_DIR


class VkBot(threading.Thread):

    def send_message(self, id, msg):
        self.vk.messages.send(peer_id=id, message=msg, access_token=self._TOKEN, random_id=get_random_id())

    def message_to_me(self, msg):
        return msg.find(self.mention) >= 0

    def parse_msg(self, msg):
        return msg.replace(self.mention + ' ', '') \
            .replace(self.mention + ', ', '') \
            .replace(self.mention + ',', '') \
            .replace('\r', '').replace('\n', '')

    def __init__(self):
        super().__init__()
        f = open(BASE_DIR + "/secrets/vk.txt", "r")
        self._TOKEN = f.readline().replace('\r', '').replace('\n', '')
        group_id = int(f.readline().replace('\r', '').replace('\n', ''))
        vk_session = vk_api.VkApi(token=self._TOKEN)
        self.longpoll = VkBotLongPoll(vk_session, group_id=group_id)
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
                        else:
                            self.send_message(event.object.peer_id, "Игорь Петрович не понял вашего ответа...")
            except Exception as e:
                # log = Log.objects.create()
                # log.msg='ОШИБКА ВЫПОЛНЕНИЯ ЛОНГПОЛА. '+str(e)
                # log.save()
                print(e)
    def run(self):
        self.listen_longpoll()
