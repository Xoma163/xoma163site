from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import get_inline_keyboard
from apps.API_VK.command.Consts import Role
from apps.API_VK.management.commands.start import cameraHandler

class Birds(CommonCommand):
    def __init__(self):
        names = ["с", "c", "синички"]
        help_text = "Синички - ссылка и гифка с синичками"
        detail_help_text = "Синички [кол-во кадров=20] - ссылка и гифка с синичками. Максимум 200 кадров"
        keyboard = [{'text': 'Синички 0', 'color': 'blue', 'row': 2, 'col': 1},
                    {'text': 'Синички 20', 'color': 'blue', 'row': 2, 'col': 2},
                    {'text': 'Синички 100', 'color': 'blue', 'row': 2, 'col': 3}]

        super().__init__(names, help_text, detail_help_text, keyboard, int_args=[0], access=Role.TRUSTED, api=False)

    def start(self):
        self.vk_bot.set_activity(self.vk_event.peer_id)
        attachments = []
        try:
            image = cameraHandler.get_img()
        except RuntimeError as e:
            print(e)
            return "какая-то дичь с синичками. Зовите разраба"
        attachment = self.vk_bot.upload_photos(image)[0]
        attachments.append(attachment)

        frames = 20
        if self.vk_event.args:
            frames = self.vk_event.args[0]
            self.check_number_arg_range(frames, 0, cameraHandler.MAX_FRAMES)

        if frames != 0:
            try:
                document = cameraHandler.get_gif(frames)
            except RuntimeError as e:
                return str(e)
            attachment = self.vk_bot.upload_document(document, self.vk_event.peer_id, "Синички")
            attachments.append(attachment)
        attachments.append('https://birds.xoma163.xyz')
        return {
            'attachments': attachments,
            "keyboard": get_inline_keyboard(self.names[0], args={"frames": frames}),
            'dont_parse_links': True
        }
