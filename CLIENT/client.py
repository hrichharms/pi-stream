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
FPS = 32


def debug(x: str):
    print(str(datetime.datetime.now()).split()[1].split(".")[0], x)


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def serialize(img: ndarray) -> bytes:
    return "|".join(["*".join([",".join(str(channel) for channel in pixel) for pixel in row]) for row in img.tolist()]).encode()


if __name__ == "__main__":

    debug("Initializing camera object and capture settings...")
    camera = PiCamera()
    camera.resolution = RESOLUTION
    camera.framerate = FPS

    debug("Initializing capture buffer...")
    raw_capture = PiRGBArray(camera, size=RESOLUTION)

    debug("Creating socket object...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    debug(f"Binding socket to {get_ip()}:{PORT}...")
    s.bind((get_ip(), PORT))

    debug(f"Connecting to server at {argv[1]}:{argv[2]}...")
    s.connect((argv[1], int(argv[2])))

    debug("Starting frame send loop...")
    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):

        # serialize and send the current frame to the viewing server
        s.send(serialize(frame.array))

        # clear raw capture array for next frame
        raw_capture.truncate(0)
