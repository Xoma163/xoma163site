import time

from django.core.management import BaseCommand

from apps.API_VK.APIs.youtube import get_youtube_channel_info
from apps.service.models import YoutubeSubscribe
from xoma163site.wsgi import vk_bot


class Command(BaseCommand):

    def __init__(self):
        super().__init__()

    def handle(self, *args, **kwargs):
        yt_subs = YoutubeSubscribe.objects.all()
        for yt_sub in yt_subs:
            yt_info = get_youtube_channel_info(yt_sub.channel_id)
            if yt_info['last_video']['date'] > yt_sub.date:
                if yt_sub.chat:
                    peer_id = yt_sub.chat.chat_id
                else:
                    peer_id = yt_sub.author.user_id
                msg = f"Новое видео на канале {yt_sub.title} - {yt_info['last_video']['title']}\n" \
                      f"{yt_info['last_video']['link']}"
                res = {'msg': msg, 'attachments': yt_info['last_video']['link']}
                vk_bot.parse_and_send_msgs(peer_id, res)
                yt_sub.date = yt_info['last_video']['date']
                yt_sub.save()
            time.sleep(2)
