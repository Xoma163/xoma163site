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
    cv2.imwrite(filename, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

    return os.path.abspath(filename)


def gif(frames=20):
    import cv2, os
    import imageio as io

    filename = "test.gif"
    temp_filename = "temp.jpg"
    capture = cv2.VideoCapture("http://xoma163.site:20000/mjpg/video.mjpg")
    i = 0
    images = []
    while capture.isOpened() and i < frames:
        ret, frame = capture.read()
        frame = cv2.resize(frame, (0, 0), fx=720 / 1600, fy=720 / 1600)
        cv2.imwrite(temp_filename, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 75])
        images.append(cv2.imread(temp_filename))
        i += 1

    io.mimsave(filename, images, duration=0.1)

    return os.path.abspath(filename)
