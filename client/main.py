import requests

import io
import cv2 
import sys 
import time 
import numpy as np
from PIL import ImageGrab


def yield_a_screenshot():
    while True:
        img = ImageGrab.grab()
        img_np = np.array(img)
        yield img_np


def yeld_rickroll_frame():
    rickroll = 'rickroll.mp4'
    video = cv2.VideoCapture(rickroll)

    while True:
        sucsess, roll_frame = video.read()
        if not sucsess:
            video = cv2.VideoCapture(rickroll)
            sucsess, roll_frame = video.read()
            if not sucsess:
                print('No rickroll(', file=sys.stderr)

        yield roll_frame


def numpy_im_to_byte_frame(frame):
    imgencode_Mask=cv2.imencode('.jpg',frame)[1]
    stringData_mask=imgencode_Mask.tostring()
    return  io.BytesIO(stringData_mask).getvalue()

g = yeld_rickroll_frame()
screen = yield_a_screenshot()

def get_frame():
    frame = next(screen)
    return numpy_im_to_byte_frame(frame)



string = "Привет мир!".encode("utf-8")
print (string)

while True:
    requests.post(url="http://127.0.0.1:8666/cach-image", 
              data=get_frame(),
              headers={'Content-Type': 'text/plain'})
    time.sleep(0.1)