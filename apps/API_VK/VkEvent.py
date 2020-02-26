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
        self.sender = vk_event['sender']
        self.chat = vk_event['chat']
        # Куда будет отправлен ответ
        self.peer_id = vk_event['peer_id']

        # Если переданы скрытые параметры с кнопок
        if 'message' in vk_event and 'payload' in vk_event['message'] and vk_event['message']['payload']:
            self.payload = json.loads(vk_event['message']['payload'])
            self.msg = None
            self.command = self.payload['command']
            if 'args' in self.payload:
                self.args = [arg for arg in self.payload['args'].values()]
            else:
                self.args = None
        else:
            self.msg = vk_event['parsed']['msg']
            self.command = vk_event['parsed']['command']
            self.args = vk_event['parsed']['args']
            self.original_args = vk_event['parsed']['original_args']
            self.keys = vk_event['parsed']['keys']
            self.keys_list = vk_event['parsed']['keys_list']
            self.params = vk_event['parsed']['params']
            self.params_without_keys = vk_event['parsed']['params_without_keys']

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
            self.api = vk_event['api']
        else:
            self.api = False
