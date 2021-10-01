import socket
import datetime
import numpy
import cv2
import pickle
import struct


PORT = 8000


def debug(x: str):
    print(str(datetime.datetime.now()).split()[1].split(".")[0], x)


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


if __name__ == "__main__":

    debug("Creating socket object...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    debug(f"Binding socket to {get_ip()}:{PORT}...")
    s.bind((get_ip(), PORT))

    debug("Awaiting client connection...")
    s.listen(1)
    conn, addr = s.accept()

    debug(f"Connection received from {addr[0]}:{addr[1]}. Starting frame display loop...")
    data = b""
    while True:

        debug("Receiving next frame...")
        while len(data) < 4:
            data += conn.recv(4096)
        message_size = struct.unpack("I", data[:4])[0]
        data = data[4:]

        while len(data) < message_size:
            data += conn.recv(4096)
        frame_data, data = data[:message_size], data[message_size:]

        debug("Deserializing frame data...")
        frame = pickle.loads(frame_data)

        debug("Rendering processed frame...")
        cv2.imshow("Frame", frame)
        cv2.waitKey(1)
