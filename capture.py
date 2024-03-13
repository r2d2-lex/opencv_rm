import numpy as np
import cv2
from mss import mss
from PIL import Image

mon = {'left': 160, 'top': 160, 'width': 1024, 'height': 768}

with mss() as sct:
    while True:
        screenShot = sct.grab(mon)
        img = Image.frombytes(
            'RGB',
            (screenShot.width, screenShot.height),
            screenShot.rgb,
        )
        cv2.imshow('test', np.array(img))
        if cv2.waitKey(33) & 0xFF in (
            ord('q'),
            27,
        ):
            break
####################################################################################

import numpy as np
import cv2
from mss import mss
from PIL import Image

bounding_box = {'top': 100, 'left': 100, 'width': 1280, 'height': 960}

sct = mss()


def main():
    while True:
        sct_img = sct.grab(bounding_box)
        cv2.imshow('screen', np.array(sct_img))

        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            break
