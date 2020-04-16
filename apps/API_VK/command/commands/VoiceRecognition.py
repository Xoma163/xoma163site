# import SpeechRecognition as SpeechRecognition
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
        super().__init__(names,
                         fwd=True
                         )

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

        # ToDo: может как-то можно обойтись без файлов
        FILENAME_MP3 = f"{audio_message['owner_id']}_{audio_message['id']}.mp3"
        FILEPATH_MP3 = f"{BASE_DIR}/static/vkapi/recognition/{FILENAME_MP3}"
        FILENAME_WAV = f"{audio_message['owner_id']}_{audio_message['id']}.wav"
        FILEPATH_WAV = f"{BASE_DIR}/static/vkapi/recognition/{FILENAME_WAV}"

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
            print("Google Speech Recognition could not understand audio")
            return "Ничего не понял(("
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            return "Проблема с форматом"
