from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import get_inline_keyboard
from xoma163site.wsgi import cameraHandler


class Birds(CommonCommand):
    def __init__(self):
        names = ["с", "c", "синички"]
        help_text = "Синички - ссылка и гифка с синичками"
        detail_help_text = "Синички [кол-во кадров=20] - ссылка и гифка с синичками. Максимум 200 кадров"
        keyboard = [{'text': 'Синички 0', 'color': 'blue', 'row': 2, 'col': 1},
                    {'text': 'Синички 20', 'color': 'blue', 'row': 2, 'col': 2},
                    {'text': 'Синички 100', 'color': 'blue', 'row': 2, 'col': 3}]

        super().__init__(names, help_text, detail_help_text, keyboard, int_args=[0], api=False)

    def start(self):
        attachments = []
        try:
            image = cameraHandler.get_img()
        except RuntimeError as e:
            print(e)
            return "какая-то дичь с синичками. Зовите разраба"
        frames = 20

        if self.vk_event.args:
            frames = self.vk_event.args[0]
            self.check_number_arg_range(frames, 0, cameraHandler.MAX_FRAMES)

        attachment = self.vk_bot.upload_photo(image)
        attachments.append(attachment)
        if frames != 0:
            try:
                document = cameraHandler.get_gif(frames)
            except RuntimeError as e:
                return str(e)
            attachment = self.vk_bot.upload_document(document, self.vk_event.peer_id, "Синички")
            attachments.append(attachment)

        return {'attachments': attachments, "keyboard": get_inline_keyboard(self.names[0], args={"frames": frames})}

        # ToDo: баг ВКАПИ, при котором при отправке ссылки атачменты не прикрепляются. Ишю 54
        # https://github.com/python273/vk_api/issues/329
        # return {'msg': "http://birds.xoma163.xyz", 'attachments': attachments}
