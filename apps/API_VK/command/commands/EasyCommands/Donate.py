from apps.API_VK.command.CommonCommand import CommonCommand


class Donate(CommonCommand):
    def __init__(self):
        names = ["донат"]
        help_text = "Донат - ссылка на донат"
        super().__init__(names, help_text)

    def start(self):
        attachment = self.vk_bot.get_attachment_by_id('photo', None, 457243301)
        url = 'https://www.donationalerts.com/r/xoma163'
        return {'msg': url, 'attachments': [attachment, url]}
