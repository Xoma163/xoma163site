import datetime
import os
import threading
import time

import cv2


class CameraHandler(threading.Thread):
    def _init_my_lists(self):
        self.images = MaxSizeList(self.MAX_FRAMES)
        self.images.init_frames()
        self.time_on_frame = MaxSizeList(self.MAX_FRAMES)
        self.time_on_frame.init_0()

    def __init__(self, MAX_FRAMES=100):
        super().__init__()
        self.MAX_FRAMES = MAX_FRAMES
        self._MAX_WIDTH = 1600
        self._running = True
        self.gif = None
        self.SCALED_WIDTH = 480
        self._init_my_lists()

    def run(self):
        capture = cv2.VideoCapture("http://192.168.1.44/mjpg/video.mjpg")

        time1 = time.time()
        while capture.isOpened():
            while self._running:
                delta_time = time.time() - time1
                # print(delta_time)
                self.time_on_frame.push(delta_time * 1000)  # мс
                fps = round(1 / delta_time, 1)
                time1 = time.time()

                ret, frame = capture.read()
                frame = cv2.resize(frame, (0, 0), fx=self.SCALED_WIDTH/self._MAX_WIDTH, fy=self.SCALED_WIDTH/self._MAX_WIDTH)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                frame = self.draw_text_on_image(frame, datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S"), (10, 20))
                frame = self.draw_text_on_image(frame, str(fps) + " FPS", (frame.shape[1] - 80, 20))
                self.images.push(frame)
            else:
                self.wait()
        else:
            self.wait()

    def terminate(self):
        self._running = False

    def resume(self):
        self._running = True

    def is_active(self):
        return self._running

    @staticmethod
    def wait():
        time.sleep(1)

    def get_gif(self, frames=20, offline_mode=False):
        if offline_mode:
            self.resume()
            self._init_my_lists()
            while self.time_on_frame.get_list_size(frames)[0] == 0:
                self.wait()
            self.terminate()

        filename = "static/vkapi/birds.gif"
        images = self.images.get_list_size(frames)
        frametimes = self.time_on_frame.get_list_size(frames)
        # Второй способ
        # duration = sum(self.time_on_frame.get_list_size(frames)) / frames
        # imageio.mimsave(filename, images, duration=duration)
        from PIL import Image

        pil_images = []
        for i in range(len(images)):
            pil_image = Image.fromarray(images[i])
            # Делаю это потому что в Pillow есть баг, который не позволяет указать list duration в .save
            pil_image.info['duration']=frametimes[i]
            pil_images.append(pil_image)

        pil_images[0].save(filename,
                           save_all=True,
                           append_images=pil_images[1:],
                           loop=0,
                           # optimize=True,
                           )
        return os.path.abspath(filename)

    def get_img(self):
        filename = "static/vkapi/snapshot.jpg"
        frame = self.images.get_last()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        cv2.imwrite(filename, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
        return os.path.abspath(filename)

    @staticmethod
    def draw_text_on_image(image, text, pos):
        cv2.putText(image, text, pos, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 4)
        cv2.putText(image, text, pos, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        return image


class MaxSizeList(object):

    def __init__(self, max_length):
        self.max_length = max_length
        self.ls = []

    def init_frames(self):
        filename = "static/vkapi/snapshot.jpg"
        frame = cv2.imread(filename)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        # Frame convert to ndarray
        self.ls = [frame for i in range(self.max_length)]

    def init_0(self):
        self.ls = [0 for i in range(self.max_length)]

    def push(self, st):
        if len(self.ls) == self.max_length:
            self.ls.pop(0)
        self.ls.append(st)

    def get_list(self):
        return self.ls

    def get_list_size(self, size):
        return self.ls[self.max_length - size:self.max_length]

    def get_last(self):
        return self.ls[self.max_length - 1]
