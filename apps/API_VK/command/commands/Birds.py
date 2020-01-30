from apps.API_VK.command.CommonCommand import CommonCommand
from xoma163site.wsgi import cameraHandler


class Birds(CommonCommand):
    def __init__(self):
        names = ["с", "c", "синички"]
        help_text = "Синички - ссылка и гифка с синичками"
        detail_help_text = "Синички ([N[,M]]) - ссылка и гифка с синичками. N - количество кадров в гифке, M - качество(0 или 1). По умолчанию N=100,M=0"
        keyboard = [{'text': 'Синички 0', 'color': 'blue', 'row': 2, 'col': 1},
                    {'text': 'Синички 20', 'color': 'blue', 'row': 2, 'col': 2},
                    {'text': 'Синички 100', 'color': 'blue', 'row': 2, 'col': 3}]

        super().__init__(names, help_text, detail_help_text, check_int_args=[0, 1], keyboard=keyboard, api=False)

    def start(self):
        attachments = []
        try:
            path = cameraHandler.get_img()
        except RuntimeError as e:
            print(e)
            return "какая-то дичь с синичками. Зовите разраба"
        frames = 20
        quality = 0

        if self.vk_event.args:
            frames = self.vk_event.args[0]
            self.check_int_arg_range(frames, 0, cameraHandler.MAX_FRAMES)
            if len(self.vk_event.args) > 1:
                quality = self.vk_event.args[1]
                self.check_int_arg_range(quality, 0, 1)

        photo = self.vk_bot.upload.photo_messages(path)[0]
        cameraHandler.clear_file(path)
        attachments.append(f"photo{photo['owner_id']}_{photo['id']}")

        if frames != 0:
            try:
                path2 = cameraHandler.get_gif(frames, quality == 1)
            except RuntimeError as e:
                return str(e)
            gif = self.vk_bot.upload.document_message(path2, title='Синички', peer_id=self.vk_event.peer_id)['doc']
            cameraHandler.clear_file(path2)
            attachments.append(f"doc{gif['owner_id']}_{gif['id']}")
        return {'msg': '', 'attachments': attachments}
        # ToDo: баг ВКАПИ, при котором при отправке ссылки атачменты не прикрепляются. Ишю 54
        # return {'msg': "http://birds.xoma163.xyz", 'attachments': attachments}
