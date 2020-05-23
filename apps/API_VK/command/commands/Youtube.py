import requests
from bs4 import BeautifulSoup

from apps.API_VK.APIs.youtube import get_youtube_channel_info
from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import check_user_group
from apps.API_VK.command.Consts import Role
from apps.API_VK.models import VkUser
from apps.service.models import YoutubeSubscribe


def get_users(chat, who):
    params = {'chats': chat, 'groups__name': who}
    return list(VkUser.objects.filter(**params))


MAX_USER_SUBS_COUNT = 3


class YouTube(CommonCommand):
    def __init__(self):
        names = ["ютуб", 'youtube']
        help_text = "Ютуб - создаёт подписку на ютуб канал"
        detail_help_text = \
            "Ютуб добавить (id/название канала) - создаёт подписку на канал. Бот пришлёт тебе новое видео с канала \n" \
            f"Ютуб удалить (название канала) - удаляет подписку на канал. " \
            f"(если в конфе, то только по конфе, в лс только по лс). Максимум подписок - {MAX_USER_SUBS_COUNT} шт.\n" \
            "Ютуб подписки - пришлёт твои активные подписки (если в конфе, то только подписки по конфе)\n" \
            "Ютуб конфа - пришлёт активные подписки по конфе\n" \
            "\n" \
            "Чтобы узнать id канала нужно перейти на канал и скопировать содержимое после " \
            "https://www.youtube.com/channel/**********\n" \
            "Чтобы узнать название канала, нужно перейти на канал и скопировать содержимое после " \
            "https://www.youtube.com/user/********** или https://www.youtube.com/**********\n\n" \
            "Проверка новых видео проходит каждый час"
        super().__init__(names, help_text, detail_help_text, args=1)

    def start(self):
        action = self.vk_event.args[0]
        if action in ['добавить', 'подписаться', 'подписка']:
            self.check_args(2)
            channel_id = self.vk_event.args[1]
            try:
                url = f'https://youtube.com/user/{channel_id}'
                response = requests.get(url)
                bsop = BeautifulSoup(response.content, 'html.parser')
                channel_id = bsop.find_all('link', {'rel': 'canonical'})[0].attrs['href'].split('/')[-1]
            except Exception:
                pass

            if self.vk_event.chat:
                existed_sub = YoutubeSubscribe.objects.filter(chat=self.vk_event.chat,
                                                              channel_id=channel_id)
            else:
                existed_sub = YoutubeSubscribe.objects.filter(chat__isnull=True,
                                                              channel_id=channel_id)
            if existed_sub.exists():
                return f"Ты уже и так подписан на канал {existed_sub.first().title}"

            user_subs_count = YoutubeSubscribe.objects.filter(author=self.vk_event.sender).count()

            # Ограничение 3 подписки для нетрастед
            if not check_user_group(self.vk_event.sender, Role.TRUSTED.name) and user_subs_count >= MAX_USER_SUBS_COUNT:
                return f"Максимальное число подписок - {MAX_USER_SUBS_COUNT}"

            youtube_info = get_youtube_channel_info(channel_id)
            yt_sub = YoutubeSubscribe(
                author=self.vk_event.sender,
                chat=self.vk_event.chat,
                channel_id=channel_id,
                title=youtube_info['title'],
                date=youtube_info['last_video']['date']
            )
            yt_sub.save()
            return f'Подписал на канал {youtube_info["title"]}'
        elif action in ['удалить', 'отписаться', 'отписка']:
            self.check_args(2)
            channel_title = self.vk_event.args[1]
            yt_sub = self.get_sub(channel_title, True)
            yt_sub_title = yt_sub.title
            yt_sub.delete()
            return f"Удалил подписку на канал {yt_sub_title}"
        elif action in ['подписки']:
            return self.get_subs()
        elif action in ['конфа']:
            self.check_conversation()
            return self.get_subs(conversation=True)

    def get_sub(self, channel, for_delete=False):
        if self.vk_event.chat:
            yt_subs = YoutubeSubscribe.objects.filter(chat=self.vk_event.chat)
            if self.vk_event.chat.admin != self.vk_event.sender:
                yt_subs = yt_subs.filter(author=self.vk_event.sender)
        else:
            yt_subs = YoutubeSubscribe.objects.filter(author=self.vk_event.sender)
            if for_delete:
                yt_subs = yt_subs.filter(chat__isnull=True)
        yt_subs = yt_subs.filter(title__icontains=channel)

        yt_subs_count = yt_subs.count()
        if yt_subs_count == 0:
            raise RuntimeWarning("Не нашёл :(")
        elif yt_subs_count == 1:
            return yt_subs.first()
        else:
            yt_subs = yt_subs[:10]
            yt_subs_titles = [yt_sub.title for yt_sub in yt_subs]
            yt_subs_titles_str = ";\n".join(yt_subs_titles)

            msg = f"Нашёл сразу {yt_subs_count}. уточните:\n\n" \
                  f"{yt_subs_titles_str}" + '.'
            if yt_subs_count > 10:
                msg += f"\n..."
            raise RuntimeWarning(msg)

    def get_subs(self, conversation=False):
        if conversation:
            yt_subs = YoutubeSubscribe.objects.filter(chat=self.vk_event.chat)
        else:
            yt_subs = YoutubeSubscribe.objects.filter(author=self.vk_event.sender)
            if self.vk_event.chat:
                yt_subs = yt_subs.filter(chat=self.vk_event.chat)
        if yt_subs.count() == 0:
            return "Нет активных подписок"

        yt_subs_titles_str = ""
        for yt_sub in yt_subs:
            yt_subs_titles_str += yt_sub.title
            if not conversation and yt_sub.chat:
                yt_subs_titles_str += f" (конфа - {yt_sub.chat})"
            yt_subs_titles_str += '\n'

        return yt_subs_titles_str
