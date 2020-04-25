import json
import re

from secrets.secrets import secrets


def auto_str(cls):
    def __str__(self):
        return '%s(%s)' % (
            type(self).__name__, ', '.join('%s=%s' % item for item in vars(self).items())
        )

    cls.__str__ = __str__
    return cls


@auto_str
class VkEvent:

    @staticmethod
    def delete_slash_and_mentions(msg, mentions):
        # Обрезаем палку
        if len(msg) > 0:
            if msg[0] == '/':
                msg = msg[1:]
            for mention in mentions:
                msg = msg.replace(mention, '')
        return msg

    @staticmethod
    def parse_msg(msg):
        # Сообщение, команда, аргументы, аргументы строкой, ключи
        """
        msg - оригинальное сообщение
        command - команда
        args - список аргументов
        original_args - строка аргументов (без ключей)
        params - оригинальное сообщение без команды (с аргументами и ключами)

        """
        msg_clear = re.sub(" +", " ", msg)
        msg_clear = re.sub(",+", ",", msg_clear)
        msg_clear = msg_clear.strip().strip(',').strip().strip(' ').strip().replace('ё', 'е')

        msg_dict = {'msg': msg,
                    'msg_clear': msg_clear,
                    'command': None,
                    'args': None,
                    'original_args': None,
                    }

        command_arg = msg_clear.split(' ', 1)
        msg_dict['command'] = command_arg[0].lower()
        if len(command_arg) > 1:
            if len(command_arg[1]) > 0:
                msg_dict['args'] = command_arg[1].split(' ')
                msg_dict['original_args'] = command_arg[1].strip()

        return msg_dict

    def parse_attachments(self, vk_attachments):
        attachments = []

        if vk_attachments:
            for attachment in vk_attachments:
                attachment_type = attachment[attachment['type']]

                new_attachment = {
                    'type': attachment['type']
                }
                if 'owner_id' in attachment_type:
                    new_attachment['owner_id'] = attachment_type['owner_id']
                if 'id' in attachment_type:
                    new_attachment['id'] = attachment_type['id']
                if attachment['type'] in ['photo', 'video', 'audio', 'doc']:
                    new_attachment[
                        'vk_url'] = f"{attachment['type']}{attachment_type['owner_id']}_{attachment_type['id']}"
                    new_attachment['url'] = f"https://vk.com/{new_attachment['vk_url']}"
                if attachment['type'] == 'photo':
                    max_size_image = attachment_type['sizes'][0]
                    max_size_width = max_size_image['width']
                    for size in attachment_type['sizes']:
                        if size['width'] > max_size_width:
                            max_size_image = size
                            max_size_width = size['width']
                        new_attachment['download_url'] = max_size_image['url']
                        new_attachment['size'] = {
                            'width': max_size_image['width'],
                            'height': max_size_image['height']}
                elif attachment['type'] == 'video':
                    new_attachment['title'] = attachment_type['title']
                elif attachment['type'] == 'audio':
                    new_attachment['artist'] = attachment_type['artist']
                    new_attachment['title'] = attachment_type['title']
                    new_attachment['duration'] = attachment_type['duration']
                    new_attachment['download_url'] = attachment_type['url']
                elif attachment['type'] == 'doc':
                    new_attachment['title'] = attachment_type['title']
                    new_attachment['ext'] = attachment_type['ext']
                    new_attachment['download_url'] = attachment_type['url']
                elif attachment['type'] == 'wall':
                    if 'attachments' in attachment_type:
                        new_attachment['attachments'] = self.parse_attachments(attachment_type['attachments'])
                    elif 'copy_history' in attachment_type and len(
                            attachment_type['copy_history']) > 0 and 'attachments' in \
                            attachment_type['copy_history'][0]:
                        new_attachment['attachments'] = self.parse_attachments(
                            attachment_type['copy_history'][0]['attachments'])
                elif attachment['type'] == 'audio_message':
                    new_attachment['download_url'] = attachment_type['link_mp3']
                    new_attachment['duration'] = attachment_type['duration']
                elif attachment['type'] == 'link':
                    new_attachment['url'] = attachment_type['url']
                    new_attachment['title'] = attachment_type['title']
                    new_attachment['description'] = attachment_type['description']
                    new_attachment['caption'] = attachment_type['caption']

                attachments.append(new_attachment)

        if attachments and len(attachments) > 0:
            return attachments
        else:
            return None

    def __init__(self, vk_event):
        self.mentions = secrets['vk']['bot']['mentions']

        vk_event['message']['text'] = self.delete_slash_and_mentions(vk_event['message']['text'], self.mentions)
        vk_event['parsed'] = self.parse_msg(vk_event['message']['text'])
        vk_event['attachments'] = self.parse_attachments(vk_event.get('message').get('attachments'))

        self.sender = vk_event.get('sender')
        self.chat = vk_event.get('chat')
        self.peer_id = vk_event.get('peer_id')

        # Если переданы скрытые параметры с кнопок
        if 'message' in vk_event and 'payload' in vk_event['message'] and vk_event['message']['payload']:
            self.payload = json.loads(vk_event['message']['payload'])
            self.msg = None
            self.command = self.payload['command']
            if 'args' in self.payload:
                if isinstance(self.payload['args'], dict):
                    self.args = [arg for arg in self.payload['args'].values()]
                elif isinstance(self.payload['args'], list):
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
            self.payload = None

        self.action = vk_event.get('message').get('action')

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
