import io

import requests
import speech_recognition as sr
from pydub import AudioSegment

from apps.API_VK.command.CommonCommand import CommonCommand

MAX_DURATION = 20


class VoiceRecognition(CommonCommand):
    def __init__(self):
        names = ["распознай", "голос", "голосовое"]
        help_text = "Распознай - распознаёт голосовое сообщение"
        detail_help_text = "Распознай (Пересланное сообщение с голосовым сообщением) - распознаёт голосовое " \
                           "сообщение\n" \
                           "Если дан доступ к переписке, то распознает автоматически"
        super().__init__(names, help_text, detail_help_text)

    def accept(self, vk_event):
        if vk_event.attachments:
            for attachment in vk_event.attachments:
                if attachment['type'] == 'audio_message':
                    return True

        if vk_event.command in self.names:
            return True
        return False

    def start(self):
        from apps.API_VK.command.CommonMethods import get_attachments_from_attachments_or_fwd
        audio_messages = get_attachments_from_attachments_or_fwd(self.vk_event, 'audio_message')
        if not audio_messages:
            return "Не нашёл голосового сообщения"
        audio_message = audio_messages[0]

        response = requests.get(audio_message['download_url'], stream=True)
        i = io.BytesIO(response.content)
        i.seek(0)
        o = io.BytesIO()
        o.name = "recognition.wav"
        AudioSegment.from_file(i, 'mp3').export(o, format='wav')
        o.seek(0)

        r = sr.Recognizer()
        with sr.AudioFile(o) as source:
            audio = r.record(source)

        try:
            msg = r.recognize_google(audio, language='ru_RU')
            return msg
        except sr.UnknownValueError:
            return "Ничего не понял(("
        except sr.RequestError as e:
            print(str(e))
            return "Проблема с форматом"
