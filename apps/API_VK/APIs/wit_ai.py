from tempfile import TemporaryFile

import requests

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


def get_text_from_audio_file(audio_message):
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
