import io

import requests
import speech_recognition as sr
from pydub import AudioSegment

from apps.API_VK.VkEvent import VkEvent
from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import get_attachments_from_attachments_or_fwd

MAX_DURATION = 20


def have_audio_message(vk_event):
    if isinstance(vk_event, VkEvent):
        all_attachments = vk_event.attachments or []
        if vk_event.fwd:
            all_attachments += vk_event.fwd[0]['attachments']
        if all_attachments:
            for attachment in all_attachments:
                if attachment['type'] == 'audio_message':
                    return True
    else:
        all_attachments = vk_event['message']['attachments'].copy()
        if vk_event['fwd']:
            all_attachments += vk_event['fwd'][0]['attachments']
        if all_attachments:
            for attachment in all_attachments:
                if attachment['type'] == 'audio_message':
                    # Костыль, чтобы при пересланном сообщении он не выполнял никакие другие команды
                    vk_event['message']['text'] = ''
                    return True
    return False


class VoiceRecognition(CommonCommand):
    def __init__(self):
        names = ["распознай", "голос", "голосовое"]
        help_text = "Распознай - распознаёт голосовое сообщение"
        detail_help_text = "Распознай (Пересланное сообщение с голосовым сообщением) - распознаёт голосовое " \
                           "сообщение\n" \
                           "Если дан доступ к переписке, то распознает автоматически"
        super().__init__(names, help_text, detail_help_text)

    def accept(self, vk_event):
        if have_audio_message(vk_event):
            return True
        if vk_event.command in self.names:
            return True

        return False

    def start(self):
        audio_messages = get_attachments_from_attachments_or_fwd(self.vk_event, 'audio_message')
        if not audio_messages:
            return "Не нашёл голосового сообщения"
        self.vk_bot.set_activity(self.vk_event.peer_id, 'audiomessage')

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
