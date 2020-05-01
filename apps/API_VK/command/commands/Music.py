import io

import requests
import youtube_dl
from pydub import AudioSegment

from apps.API_VK.command.CommonCommand import CommonCommand


class NothingLogger(object):
    @staticmethod
    def debug(msg):
        pass

    @staticmethod
    def warning(msg):
        pass

    @staticmethod
    def error(msg):
        print(msg)


class Music(CommonCommand):
    def __init__(self):
        names = ["музыка"]
        help_text = "Музыка - скачивает аудиодорожку из YouTube и присылает её в виде аудио"
        detail_help_text = "Музыка (ссылка на видео youtube) - скачивает аудиодорожку из YouTube и присылает её в " \
                           "виде аудио. Продолжительность видео максимум 10 минут"
        super().__init__(names, help_text, detail_help_text, args=1)

    def start(self):
        self.vk_bot.set_activity(self.vk_event.peer_id, 'audiomessage')
        url = self.vk_event.args[0]
        ydl_params = {
            'outtmpl': '%(id)s%(ext)s',
            'logger': NothingLogger()
        }
        ydl = youtube_dl.YoutubeDL(ydl_params)
        ydl.add_default_info_extractors()

        try:
            video_info = ydl.extract_info(url, download=False)
        except youtube_dl.utils.DownloadError:
            return "Не смог найти видео по этой ссылке"
        audio_urls = []
        if video_info['duration'] > 600:
            return "Нельзя грузить музяку > 10 минут"
        if 'formats' in video_info:
            for _format in video_info['formats']:
                if _format['ext'] == 'm4a':
                    audio_urls.append(_format)

        if len(audio_urls) == 0:
            return "Чёт проблемки, напишите разрабу и пришлите ссылку на видео"
        max_asr_i = 0
        max_asr = audio_urls[0]['asr']
        for i, audio_url in enumerate(audio_urls):
            if audio_url['asr'] > max_asr:
                max_asr = audio_url['asr']
                max_asr_i = i
        if 'fragment_base_url' in audio_urls[max_asr_i]:
            audio_link = audio_urls[max_asr_i]['fragment_base_url']
        else:
            audio_link = audio_urls[max_asr_i]['url']

        artist = video_info['uploader']
        title = video_info['title']
        dashs = ['-', '—', '–', '−']
        for dash in dashs:
            first_dash = video_info['title'].find(dash)
            if first_dash != -1:
                artist = video_info['title'][0:first_dash].strip()
                title = video_info['title'][first_dash + 1:].strip()
                break

        response = requests.get(audio_link)
        i = io.BytesIO(response.content)
        i.seek(0)
        o = io.BytesIO()
        o.name = "audio.mp3"
        AudioSegment.from_file(i, 'm4a').export(o, format='mp3')

        try:
            audio_attachment = self.vk_bot.upload_audio(o, artist, title)
        except RuntimeError as e:
            msg = f"{str(e)}\n\nСсылка на скачивание: {audio_link}"
            return msg

        return {'attachments': audio_attachment}
