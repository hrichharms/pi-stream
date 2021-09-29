from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import socket
import datetime
from numpy import ndarray
from sys import argv


PORT = 8000
RESOLUTION = (640, 480)


def debug(x: str):
    print(str(datetime.datetime.now()).split()[1].split(".")[0], x)


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def serialize(img: ndarray) -> bytes:
    return "|".join(["*".join([",".join(str(channel) for channel in pixel) for pixel in row]) for row in img.tolist()]).encode()


if __name__ == "__main__":

    # create socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((get_ip(), PORT))

    # connect to server
    s.connect((argv[1], argv[2]))

    # get camera object
    camera = PiCamera()

    # set camera resolution
    camera.resolution = RESOLUTION

    # set fps
    camera.framerate = 32

    # array to store camera frame data
    raw_capture = PiRGBArray(camera, size=RESOLUTION)

    # continous capture loop
    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):

        # serialize and send the current frame to the viewing server
        s.send(serialize(frame.array))

        # clear raw capture array for next frame
        raw_capture.truncate(0)
