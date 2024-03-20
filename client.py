import asyncio
import pickle
import numpy as np
import cv2
import time

import pyautogui

# from server2 import HOST, PORT
from server2 import PORT
HOST = '127.0.0.1'

CHUNK = 65536
img = None
WINDOWS_NAME = 'Test'


def on_mouse(event, x, y, flags, param):
    global mouse_x, mouse_y
    if event == cv2.EVENT_LBUTTONDBLCLK:
        mouse_x, mouse_y = x, y
        print(f'EVENT_LBUTTONDBLCLK X: {mouse_x}, Y {mouse_y}')
        # time.sleep(1)
        # pyautogui.move(mouse_x, mouse_y)
        # pyautogui.doubleClick(mouse_x, mouse_y)

    elif event == cv2.EVENT_LBUTTONDOWN:
        mouse_x, mouse_y = x, y
        print(f'EVENT_LBUTTONDOWN X: {mouse_x}, Y {mouse_y}')

    elif event == cv2.EVENT_RBUTTONDOWN:
        mouse_x, mouse_y = x, y
        print(f'EVENT_RBUTTONDOWN X: {mouse_x}, Y {mouse_y}')


async def run_client() -> None:
    reader, writer = await asyncio.open_connection(HOST, PORT)

    num_frames = 0
    start = time.time()
    while True:
        num_frames += 1

        try:
            packet = await reader.readline()
        except ValueError:
            # separator exception
            print('Cant read size of object')
            continue

        size_of_image = int(packet.decode().rstrip())

        data = []
        loaded_size = size_of_image
        while True:
            if loaded_size > CHUNK:
                data_part = await reader.read(CHUNK)
            else:
                data_part = await reader.read(loaded_size)

            if not data_part:
                print('Break')
                break
            loaded_size = loaded_size - len(data_part)
            data.append(data_part)
            data_size = len(data)
            if data_size >= size_of_image:
                break
            if not loaded_size:
                break

        img = pickle.loads(b"".join(data))

        # cv2.namedWindow(WINDOWS_NAME, cv2.WND_PROP_FULLSCREEN)
        # cv2.setWindowProperty(WINDOWS_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.namedWindow(WINDOWS_NAME, flags=cv2.WINDOW_GUI_NORMAL)
        cv2.imshow(WINDOWS_NAME, np.array(img))
        cv2.setMouseCallback(WINDOWS_NAME, on_mouse)

        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            break
        end = time.time()
        seconds = end - start
        fps = num_frames / seconds
        # print("FPS : {0}".format(fps))
    return


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(run_client())
