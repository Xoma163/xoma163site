from tempfile import TemporaryFile

import requests

from apps.API_VK.command.CommonCommand import CommonCommand
from secrets.secrets import secrets

API_KEY = secrets['wit']['api_key']


def stream_audio_file(_bytes, chunk_size=4096):
    audio_file_temp = TemporaryFile()
    audio_file_temp.write(_bytes)
    audio_file_temp.flush()
    audio_file_temp.seek(0)
    while 1:
        data = audio_file_temp.read(chunk_size)
        if not data:
            break
        yield data


class VoiceRecognition(CommonCommand):
    def __init__(self):
        names = ["распознай", "голос", "голосовое"]
        super().__init__(names, fwd=True)

    def start(self):
        from apps.API_VK.VkBotClass import parse_attachments

        attachments = parse_attachments(self.vk_event.fwd[0]['attachments'])
        audio_message = None
        for attachment in attachments:
            if attachment['type'] == 'audio_message':
                audio_message = attachment
                break
        if not audio_message:
            return "Не нашел аудио в пересланных сообщениях"

        r = requests.get(audio_message['download_url'], stream=True)

        URL = 'https://api.wit.ai/speech'
        headers = {'Accept': 'audio/x-mpeg-3',
                   'Authorization': 'Bearer ' + API_KEY,
                   'Content-Type': 'audio/mpeg3',
                   }
        # data = stream_audio_file(r.content)

        response = requests.post(URL, data=r.content, headers=headers, stream=True).json()
        if 'error' in response:
            return f"Ошибка распознования - {response['error']}"
        if '_text' in response and response['_text'] != "":
            return response['_text']
        else:
            return "Ничего не понял(("
