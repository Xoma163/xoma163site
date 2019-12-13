import os

from apps.API_VK.command.CommonCommand import CommonCommand
from xoma163site.settings import BASE_DIR


class Find(CommonCommand):
    def __init__(self):
        names = ["поиск", "найди", "мем"]
        help_text = "̲П̲̲̲о̲и̲с̲к [N] (N - поисковый запрос) - ищет информацию по картинкам"

        super().__init__(names, check_args=True)

    def start(self):
        import requests

        query = self.vk_event.original_args
        count = 3

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
            self.vk_bot.send_message(self.vk_event.chat_id, "Не так часто")
            return

        response = r.json().get('data').get('result').get('items')
        urls = [r.get('media') for r in response]
        if len(urls) == 0:
            self.vk_bot.send_message(self.vk_event.chat_id, "Ничего не нашёл")
            return
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
                os.remove(path)
            if len(attachments) >= count:
                break

        self.vk_bot.send_message(self.vk_event.chat_id, 'Лови', attachments=attachments)
    #
    # if len(urls) == 0:
    #     self.vk_bot.send_message(self.vk_event.chat_id, "Ничего не нашёл")
    #     return
    # msg = ""
    # for url in urls:
    #     msg += "{}\n".format(url)
    #
    # self.vk_bot.send_message(self.vk_event.chat_id, msg)
