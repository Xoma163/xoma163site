from apps.API_VK.command.CommonCommand import CommonCommand


class Help(CommonCommand):
    def __init__(self):
        names = ["помощь", "хелп", "ман", "команды", "помоги", "памаги", "спаси", "хелб", "манул", "help", "start"]
        super().__init__(names)

    def start(self):
        from apps.API_VK.command import get_help_admin_texts, get_help_moderator_texts, get_help_student_texts, \
            get_help_texts

        # self.vk_bot.send_message(self.vk_event.chat_id, get_help_text(self.vk_event.sender.is_admin, self.vk_event.sender.is_student))

        help_text = "\n— общие команды —\n"
        help_text += get_help_texts()
        help_text += "\n"
        if self.vk_event.sender.is_student:
            help_text += "\n— команды для группы 6221 —\n"
            help_text += get_help_student_texts()
        if self.vk_event.sender.is_moderator:
            help_text += "\n— команды для модераторов —\n"
            help_text += get_help_moderator_texts()
        if self.vk_event.sender.is_admin:
            help_text += "\n— команды для администраторов —\n"
            help_text += get_help_admin_texts()

        self.vk_bot.send_message(self.vk_event.chat_id, help_text)
        print(help_text)

        # print(get_commands())
