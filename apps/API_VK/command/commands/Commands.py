from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import check_user_group
from apps.API_VK.command.Consts import Role


class Commands(CommonCommand):
    def __init__(self):
        names = ["команды"]
        help_text = "команды - список всех команд"
        super().__init__(names, help_text)

    def start(self):

        from apps.API_VK.command import HELP_TEXT, API_HELP_TEXT

        if self.vk_event.from_api:
            help_texts = API_HELP_TEXT
        else:
            help_texts = HELP_TEXT

        ordered_roles = [
            {"role": Role.USER, "text": "общие команды"},
            {"role": Role.ADMIN, "text": "команды для администраторов"},
            {"role": Role.MODERATOR, "text": "команды для модераторов"},
            {"role": Role.MINECRAFT, "text": "команды для игроков майнкрафта"},
            {"role": Role.TRUSTED, "text": "команды для доверенных пользователей"},
            {"role": Role.STUDENT, "text": "команды для группы 6221"},
            {"role": Role.MINECRAFT_NOTIFY, "text": "команды для уведомлённых майнкрафтеров"},
            {"role": Role.TERRARIA, "text": "команды для игроков террарии"},
        ]
        output = ""
        for role in ordered_roles:
            if check_user_group(self.vk_event.sender, role['role']) and help_texts[role['role'].name]:
                output += f"\n\n— {role['text']} —\n"
                output += help_texts[role['role'].name]
        if help_texts['games']:
            output += "\n\n— игры —\n"
            output += help_texts['games']
        output = output.rstrip()
        return output
