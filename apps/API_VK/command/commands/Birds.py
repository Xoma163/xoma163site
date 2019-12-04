from apps.API_VK.command.CommonCommand import CommonCommand
from xoma163site.wsgi import cameraHandler


class Birds(CommonCommand):
    def __init__(self):
        names = ["с", "c", "синички"]
        help_text = "̲С̲и̲н̲и̲ч̲к̲и [N[,M]](N - количество кадров в гифке, 20 дефолт, M - качество(0 или 1), 0 дефолт) - ссылка, снапшот и гифка"
        super().__init__(names, help_text)

    def start(self):
        attachments = []
        try:
            # path = snapshot()
            path = cameraHandler.get_img()
        except RuntimeError as e:
            print(e)
            self.vk_bot.send_message(self.vk_event.chat_id, "какая-то дичь с синичками. Зовите разраба")
            return
        frames = 20
        quality = 0

        try:
            if self.vk_event.args:
                try:
                    frames = int(self.vk_event.args[0])
                    if frames > cameraHandler.MAX_FRAMES:
                        self.vk_bot.send_message(self.vk_event.chat_id,
                                                 "Ты совсем поехавший? До {} кадров давай".format(
                                                     cameraHandler.MAX_FRAMES))
                        return
                except:
                    self.vk_bot.send_message(self.vk_event.chat_id, "Введите количество кадров в gif")
                    return
                if len(self.vk_event.args) > 1:
                    try:
                        quality = int(self.vk_event.args[1])
                        if not 0 <= quality <= 1:
                            self.vk_bot.send_message(self.vk_event.chat_id, "Качество может быть в диапазоне [0,1]")
                            return
                    except:
                        self.vk_bot.send_message(self.vk_event.chat_id, "Качество может быть в диапазоне [0,1]")
                        return
        except:
            pass

        photo = self.vk_bot.upload.photo_messages(path)[0]
        attachments.append('photo{}_{}'.format(photo['owner_id'], photo['id']))

        if frames != 0:
            try:
                path2 = cameraHandler.get_gif(frames, quality == 1)
            except RuntimeError as e:
                self.vk_bot.send_message(self.vk_event.chat_id, str(e))
                return
            gif = self.vk_bot.upload.document_message(path2, title='Синички', peer_id=self.vk_event.chat_id)['doc']
            attachments.append('doc{}_{}'.format(gif['owner_id'], gif['id']))

        self.vk_bot.send_message(self.vk_event.chat_id, "", attachments=attachments)

        # ToDo: баг ВКАПИ, при котором при отправке ссылки атачменты не прикрепляются. Ишю 54
        # self.vk_bot.send_message(self.vk_event.chat_id, "http://birds.xoma163.xyz", attachments=attachments)
