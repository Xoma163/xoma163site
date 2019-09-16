
from django.shortcuts import render


# Create your views here.
def index(request):
    return render(
        request,
        'birds/index.html',
        {},
    )


def snapshot():
    import cv2, os
    filename = "snapshot.jpg"

    capture = cv2.VideoCapture("http://xoma163.site:20000/mjpg/video.mjpg")
    frame = None
    if capture.isOpened():
        ret, frame = capture.read()
    cv2.imwrite(filename, frame)

    return os.path.abspath(filename)
