from picamera.array import PiRGBArray
from picamera import PiCamera
from socket import socket, AF_INET, SOCK_DGRAM
from datetime import datetime
from numpy import ndarray
from sys import argv
from pickle import dumps
from struct import pack


PORT = 8000
RESOLUTION = (640, 480)
FPS = 32


def debug(x: str):
    print(str(datetime.now()).split()[1].split(".")[0], x)


def get_ip():
    s = socket(AF_INET, SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


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

        debug("Serializing and sending current frame to server...")
        data = pickle.dumps(frame.array)
        message_size = struct.pack("I", len(data))
        s.send(message_size + data)

        debug("Truncating frame buffer for next frame...")
        raw_capture.truncate(0)
