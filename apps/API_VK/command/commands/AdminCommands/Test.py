from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.Consts import Role


class Test(CommonCommand):
    def __init__(self):
        names = ["тест", "дебан"]
        help_text = "Тест - команда для тестов всякой фигни"
        super().__init__(names, help_text, access=Role.ADMIN)

    def start(self):
        video = self.vk_bot.upload_video_by_link("https://www.youtube.com/watch?v=Ga4-7YDZTbw", "test")
        return {'attachments': video}
