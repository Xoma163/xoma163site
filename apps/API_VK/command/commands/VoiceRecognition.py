# import SpeechRecognition as SpeechRecognition
import os

import requests
from pydub import AudioSegment

from apps.API_VK.APIs.wit_ai import get_text_from_audio_file
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
        # audio_message = {'download_url': "https://psv4.userapi.com/c852420//u15045422/audiomsg/d15/80cc2f6a18.mp3",
        #                  'id': '100',
        #                  'owner_id': "15045422"}
        if not audio_message:
            return "Не нашел аудио в пересланных сообщениях"
        r = requests.get(audio_message['download_url'], stream=True)

        filename = f"{audio_message['owner_id']}_{audio_message['id']}.mp3"
        # filename2 = f"{audio_message['owner_id']}_{audio_message['id']}.wav"
        filepath = f"{BASE_DIR}/static/vkapi/recognition/{filename}"
        # filepath2 = f"{BASE_DIR}/static/vkapi/recognition/{filename2}"
        #
        song_file = open(filepath, "wb")
        song_file.write(r.content)
        song_file.close()
        try:
            song_cutted = []
            song = AudioSegment.from_mp3(filepath)

            for fragment in range(int(song.duration_seconds // MAX_DURATION) + 1):
                extract = song[MAX_DURATION * fragment * 1000:MAX_DURATION * (fragment + 1) * 1000]
                song_cutted.append(extract)
        except Exception as e:
            print(str(e))
            return "Ошибка в сохранении аудиофайла"
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)
        #
        # import speech_recognition as sr
        # AUDIO_FILE = filepath2
        #
        # use the audio file as the audio source
        # r = sr.Recognizer()
        # with sr.AudioFile(AUDIO_FILE) as source:
        #     audio = r.record(source)
        #
        # recognize speech using Wit.ai
        # try:
        #     msg = r.recognize_wit(audio, key=secrets['wit']['api_key'])
        #     print("Wit.ai thinks you said " + msg)
        # except sr.UnknownValueError:
        #     print("Wit.ai could not understand audio")
        #     return "Не понял("
        # except sr.RequestError as e:
        #     print("Could not request results from Wit.ai service; {0}".format(e))
        #     return "Проблема с форматом"
        #
        # try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        # msg = r.recognize_google(audio)
        # print("Google Speech Recognition thinks you said " + msg)
        # except sr.UnknownValueError:
        #     print("Google Speech Recognition could not understand audio")
        #     return "Не понял("
        # except sr.RequestError as e:
        #     print("Could not request results from Google Speech Recognition service; {0}".format(e))
        #     return "Проблема с форматом"
        #
        # msg = ""
        # for data in song_cutted:
        #     msg += get_text_from_audio_file(data.raw_data)

        msg = get_text_from_audio_file(r.content)

        if len(msg) == 0:
            return "Ничего не понял(("

        return msg
