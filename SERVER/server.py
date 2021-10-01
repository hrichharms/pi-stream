from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM
from datetime import datetime
from cv2 import imshow, waitKey
from pickle import loads
from struct import unpack
from sys import argv


def debug(x: str):
    print(str(datetime.datetime.now()).split()[1].split(".")[0], x)


def get_ip():
    s = socket(AF_INET, SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


if __name__ == "__main__":

    debug("Creating socket object...")
    s = socket(AF_INET, SOCK_STREAM)

    debug(f"Binding socket to {get_ip()}:{argv[1]}...")
    s.bind((get_ip(), int(argv[1])))

    debug("Awaiting client connection...")
    s.listen(1)
    conn, addr = s.accept()

    debug(f"Connection received from {addr[0]}:{addr[1]}. Starting frame display loop...")
    data = b""
    while True:

        debug("Receiving next frame...")
        while len(data) < 4:
            data += conn.recv(4096)
        message_size = unpack("I", data[:4])[0]
        data = data[4:]

        while len(data) < message_size:
            data += conn.recv(4096)
        frame_data, data = data[:message_size], data[message_size:]

        debug("Deserializing frame data...")
        frame = loads(frame_data)

        debug("Rendering processed frame...")
        imshow("Frame", frame)
        waitKey(1)
