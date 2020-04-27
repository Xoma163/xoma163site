from apps.API_VK.command.CommonCommand import CommonCommand
from secrets.secrets import secrets


class Actions(CommonCommand):
    def __init__(self):
        super().__init__([None], priority=200)

    def accept(self, vk_event):
        if vk_event.action:
            return True
        return False

    def start(self):
        print(self.vk_event.action)
        if self.vk_event.action:
            # По приглашению пользователя
            if self.vk_event.action['type'] in ['chat_invite_user', 'chat_invite_user_by_link']:
                if self.vk_event.action['member_id'] > 0:
                    user = self.vk_bot.get_user_by_id(self.vk_event.action['member_id'])
                    self.vk_bot.add_group_to_user(user, self.vk_event.chat)
                    return 'add'
                else:
                    if self.vk_event.action['member_id'] == -int(secrets['vk']['bot']['group_id']):
                        if self.vk_event.chat.admin is None:
                            self.vk_event.chat.admin = self.vk_event.sender
                            self.vk_event.chat.save()
                            return f"Администратором конфы является {self.vk_event.sender}\n" \
                                   f"Задайте имя конфы:\n" \
                                   "/конфа {Название конфы}"
                        else:
                            return "Давненько не виделись!"
                    else:
                        self.vk_bot.get_bot_by_id(self.vk_event.action['member_id'])
            # По удалению пользователя
            elif self.vk_event.action['type'] == 'chat_kick_user':
                if self.vk_event.action['member_id'] > 0:
                    user = self.vk_bot.get_user_by_id(self.vk_event.action['member_id'])
                    self.vk_bot.remove_group_from_user(user, self.vk_event.chat)
                    return 'remove'
            # По изменению чата конфы
            # elif self.vk_event.action['type'] == 'chat_title_update':
            #     self.vk_event.chat.name = self.vk_event.action['text']
            #     self.vk_event.chat.save()
