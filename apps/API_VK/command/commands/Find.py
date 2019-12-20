import os

from apps.API_VK.command.CommonCommand import CommonCommand
from xoma163site.settings import BASE_DIR


class Find(CommonCommand):
    def __init__(self):
        names = ["поиск", "найди", "мем"]
        help_text = "̲П̲̲о̲и̲с̲к [N] (N - поисковый запрос) - ищет информацию по картинкам"

        super().__init__(names, help_text, need_args=1)

    def start(self):
        import requests

        query = self.vk_event.original_args
        count = 5

        r = requests.get("https://api.qwant.com/api/search/images",
                         params={
                             'count': 20,
                             'q': query,
                             't': 'images',
                             'safesearch': 0,
                             'locale': 'ru_RU',
                             'uiv': 4
                         },
                         headers={
                             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
                         }
                         )
        if r.status_code == 429:
            return "Не так часто"

        response = r.json().get('data').get('result').get('items')
        urls = [r.get('media') for r in response]
        if len(urls) == 0:
            return "Ничего не нашёл"
        attachments = []
        for url in urls:
            path = "{}/static/vkapi/{}.jpg".format(BASE_DIR, query)
            try:
                img = requests.get(url)
                img_file = open(path, "wb")
                img_file.write(img.content)
                img_file.close()

                photo = self.vk_bot.upload.photo_messages(path)[0]
                attachments.append('photo{}_{}'.format(photo['owner_id'], photo['id']))
            except Exception as e:
                pass
            finally:
                if os.path.exists(path):
                    os.remove(path)
            if len(attachments) >= count:
                break
        # ToDo: attachments
        return {'msg': 'Лови', 'attachments': attachments}
