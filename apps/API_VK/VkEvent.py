import json


def auto_str(cls):
    def __str__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in vars(self).items())
        )

    cls.__str__ = __str__
    return cls


@auto_str
class VkEvent:
    def __init__(self, vk_event):
        self.sender = vk_event.get('sender')
        self.chat = vk_event.get('chat')
        # Куда будет отправлен ответ
        self.peer_id = vk_event.get('peer_id')

        # Если переданы скрытые параметры с кнопок
        if 'message' in vk_event and 'payload' in vk_event['message'] and vk_event['message']['payload']:
            self.payload = json.loads(vk_event['message']['payload'])
            self.msg = None
            self.command = self.payload['command']
            if 'args' in self.payload:
                if type(self.payload['args']) == dict:
                    self.args = [arg for arg in self.payload['args'].values()]
                elif type(self.payload['args']) == list:
                    self.args = self.payload['args']
                str_args = [str(arg) for arg in self.args]
                self.original_args = " ".join(str_args)
            else:
                self.args = None
        else:
            parsed = vk_event.get('parsed')
            if parsed:
                self.msg = parsed.get('msg')
                self.command = parsed.get('command')
                self.args = parsed.get('args')
                self.original_args = parsed.get('original_args')
                self.keys = parsed.get('keys')
                self.keys_list = parsed.get('keys_list')
                self.params = parsed.get('params')
                self.params_without_keys = parsed.get('params_without_keys')

            self.payload = None
        if self.chat:
            self.from_chat = True
            self.from_user = False
        else:
            self.from_user = True
            self.from_chat = False

        if 'attachments' in vk_event:
            self.attachments = vk_event['attachments']
        else:
            self.attachments = None

        if 'fwd' in vk_event:
            self.fwd = vk_event['fwd']
        else:
            self.fwd = None

        if 'api' in vk_event:
            self.from_api = vk_event['api']
        else:
            self.from_api = False

        if 'yandex' in vk_event:
            self.yandex = vk_event['yandex']
        else:
            self.yandex = None
