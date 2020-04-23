import os

import requests
import speech_recognition as sr
from pydub import AudioSegment

from apps.API_VK.command.CommonCommand import CommonCommand
from xoma163site.settings import BASE_DIR

MAX_DURATION = 20


class VoiceRecognition(CommonCommand):
    def __init__(self):
        names = ["распознай", "голос", "голосовое"]
        help_text = "Распознай - распознаёт голосовое сообщение"
        detail_help_text = "Распознай (Пересланное сообщение с голосовым сообщением) - распознаёт голосовое " \
                           "сообщение.\n" \
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
        r = requests.get(audio_message['download_url'], stream=True)

        # ToDo: может как-то можно обойтись без файлов
        FILENAME_MP3 = f"{audio_message['owner_id']}_{audio_message['id']}.mp3"
        FILEPATH_MP3 = f"{BASE_DIR}/static/TEMP/{FILENAME_MP3}"
        FILENAME_WAV = f"{audio_message['owner_id']}_{audio_message['id']}.wav"
        FILEPATH_WAV = f"{BASE_DIR}/static/TEMP/{FILENAME_WAV}"

        song_file = open(FILEPATH_MP3, "wb")
        song_file.write(r.content)
        song_file.close()
        try:
            song = AudioSegment.from_mp3(FILEPATH_MP3)
            song.export(FILEPATH_WAV, 'wav')
        except Exception as e:
            print(str(e))
            if os.path.exists(FILEPATH_WAV):
                os.remove(FILEPATH_WAV)
            return "Ошибка в сохранении аудиофайла"
        finally:
            if os.path.exists(FILEPATH_MP3):
                os.remove(FILEPATH_MP3)

        r = sr.Recognizer()
        try:
            with sr.AudioFile(FILEPATH_WAV) as source:
                audio = r.record(source)
        except Exception as e:
            print(str(e))
            return "Ошибка какая-то"

        finally:
            if os.path.exists(FILEPATH_WAV):
                os.remove(FILEPATH_WAV)

        try:
            msg = r.recognize_google(audio, language='ru_RU')
            return msg
        except sr.UnknownValueError:
            return "Ничего не понял(("
        except sr.RequestError as e:
            print(str(e))
            return "Проблема с форматом"
