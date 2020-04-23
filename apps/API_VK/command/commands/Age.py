from apps.API_VK.APIs.everypixel import get_faces_on_photo
from apps.API_VK.command.CommonCommand import CommonCommand
from apps.API_VK.command.CommonMethods import get_attachments_from_attachments_or_fwd


def draw_on_images(image_url, faces):
    import requests
    import numpy as np
    import cv2

    resp = requests.get(image_url, stream=True).raw
    _image = np.asarray(bytearray(resp.read()), dtype="uint8")
    _image = cv2.imdecode(_image, cv2.IMREAD_COLOR)

    # B G R
    color = {'red': (0, 0, 255), 'black': (0, 0, 0), 'white': (255, 255, 255)}
    thickness = {'big': 6, 'medium': 2, 'small': 1}
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = {'big': 1, 'medium': 0.8, 'small': 0.6}

    for face in faces:
        start_point = (int(face['bbox'][0]), int(face['bbox'][1]))
        end_point = (int(face['bbox'][2]), int(face['bbox'][3]))
        if 'age' in face:
            age = str(round(face['age']))
            age_point = (int(face['bbox'][2]) - 35, int(face['bbox'][3]) - 10)
            _image = cv2.rectangle(_image, start_point, end_point, color['red'], thickness['medium'])
            _image = cv2.putText(_image, age, age_point, font, font_scale['small'], color['black'], thickness['big'])
            _image = cv2.putText(_image, age, age_point, font, font_scale['small'], color['white'], thickness['medium'])

    _bytes = cv2.imencode('.jpg', _image)[1].tostring()
    return _bytes


class Age(CommonCommand):
    def __init__(self):
        names = ["возраст"]
        help_text = "Возраст - оценить возраст людей на фотографии"
        detail_help_text = "Возраст (Изображения/Пересылаемое сообщение с изображением) - оценивает возраст людей на " \
                           "фотографии"
        super().__init__(names, help_text, detail_help_text, api=False)

    def start(self):
        images = get_attachments_from_attachments_or_fwd(self.vk_event, 'photo')

        if not images:
            return "Не нашёл картинки"
        image = images[0]
        response = get_faces_on_photo(image['download_url'])
        if response['status'] == 'error':
            if response['message'] == 'ratelimit exceeded 100 requests per 86400 seconds':
                return "Сегодняшний лимит исчерпан"
            print(response)
            return "Ошибка"
        elif response['status'] == "ok":
            if len(response['faces']) == 0:
                return "Не нашёл лиц на фото"
            file_path = draw_on_images(image['download_url'], response['faces'])
            attachments = self.vk_bot.upload_photo(file_path)
            return {"attachments": attachments}
        else:
            return "Wtf"
