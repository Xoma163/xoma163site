from datetime import datetime

import requests
from bs4 import BeautifulSoup


def get_youtube_channel_info(channel_id):
    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"

    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeWarning("Не нашёл такого канала")
    bsop = BeautifulSoup(response.content, 'html.parser')
    last_video = bsop.find_all('entry')[0]
    youtube_info = {
        'title': bsop.find('title').text,
        'last_video': {
            'title': last_video.find('title').text,
            'link': last_video.find('link').attrs['href'],
            'date': datetime.strptime(last_video.find('published').text, '%Y-%m-%dT%H:%M:%S%z'),
        }}
    return youtube_info
