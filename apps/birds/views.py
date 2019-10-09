import os
import time

from django.shortcuts import render


# Create your views here.
def index(request):
    return render(
        request,
        'birds/index.html',
        {},
    )


def snapshot():
    if not _lock_thread():
        raise RuntimeError("Падажжи, я уже делаю гифку")
    import cv2, os
    filename = "static/vkapi/snapshot.jpg"

    capture = cv2.VideoCapture("http://xoma163.site:20000/mjpg/video.mjpg")
    frame = None
    if capture.isOpened():
        ret, frame = capture.read()
    cv2.imwrite(filename, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
    _unlock_thread()
    return os.path.abspath(filename)


# ToDo: Настроить более оптимальное сжатие кадров
def gif(frames=20):
    if not _lock_thread():
        raise RuntimeError("Падажжи, я уже делаю гифку")
    import cv2, os
    import imageio as io

    filename = "static/vkapi/birds.gif"
    temp_filename = "temp.jpg"
    capture = cv2.VideoCapture("http://192.168.1.44/mjpg/video.mjpg")
    i = 0
    images = []
    time_1 = time.time()
    while capture.isOpened() and i < frames:
        ret, frame = capture.read()
        frame = cv2.resize(frame, (0, 0), fx=720 / 1600, fy=720 / 1600)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        cv2.imwrite(temp_filename, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 75])
        images.append(cv2.imread(temp_filename))
        i += 1
    time_2 = time.time()

    time_for_frame = (time_2 - time_1) / frames
    io.mimsave(filename, images, duration=time_for_frame)

    _unlock_thread()
    return os.path.abspath(filename)


filename = "static/vkapi/thread_birds.lock"


def _lock_thread():
    if not os.path.exists(filename):
        open(filename, "w")
        return True
    else:
        return False


def _unlock_thread():
    os.remove(filename)
