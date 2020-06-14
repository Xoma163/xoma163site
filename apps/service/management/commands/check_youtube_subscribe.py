import time

from django.core.management import BaseCommand

from apps.API_VK.APIs.YoutubeInfo import YoutubeInfo
from apps.API_VK.VkBotClass import VkBotClass
from apps.service.models import YoutubeSubscribe

vk_bot = VkBotClass()


class Command(BaseCommand):

    def __init__(self):
        super().__init__()

    def handle(self, *args, **kwargs):
        yt_subs = YoutubeSubscribe.objects.all()
        for yt_sub in yt_subs:
            youtube_info = YoutubeInfo(yt_sub.channel_id)
            youtube_data = youtube_info.get_youtube_channel_info()
            if youtube_data['last_video']['date'] > yt_sub.date:
                if yt_sub.chat:
                    peer_id = yt_sub.chat.chat_id
                else:
                    peer_id = yt_sub.author.user_id
                msg = f"Новое видео на канале {yt_sub.title}\n"
                video_attachment = vk_bot.upload_video_by_link(youtube_data['last_video']['link'],
                                                               youtube_data['last_video']['title'])
                res = {'msg': msg, 'attachments': video_attachment}
                vk_bot.parse_and_send_msgs(peer_id, res)
                yt_sub.date = youtube_data['last_video']['date']
                yt_sub.save()
            time.sleep(2)
