from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

# get camera object
camera = PiCamera()

# set camera resolution
camera.resolution = (640, 480)

# set fps
camera.framerate = 32

# Generates a 3D RGB array and stores it in rawCapture
raw_capture = PiRGBArray(camera, size=(640, 480))

# Wait a certain number of seconds to allow the camera time to warmup
time.sleep(0.1)

# Capture frames continuously from the camera
for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):

    # Grab the raw NumPy array representing the image
    image = frame.array

    # Display the frame using OpenCV
    cv2.imshow("Frame", image)

    # Clear the stream in preparation for the next frame
    raw_capture.truncate(0)
