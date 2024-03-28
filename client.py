import asyncio
import cv2
import pickle
import numpy as np
import threading
import time

from pynput.keyboard import Key, Listener
from queue import Queue

from config import SERVER_HOST, SERVER_PORT, DATA_PORT
from server_commands import (EVENT_MOUSEMOVE, EVENT_RBUTTONDOWN, EVENT_LBUTTONDOWN, EVENT_LBUTTONDBLCLK, QUIT_COMMAND,
                             EVENT_KB_KEY)
from utils import get_active_window_title, detect_os

CHUNK = 65536
WINDOWS_NAME = 'opencv_rm Test'
queue = Queue()
CLIENT_OS = detect_os()


def on_mouse(event, mouse_x, mouse_y, flags, param):
    # if event == cv2.EVENT_MOUSEMOVE:
    #     command = f'{EVENT_MOUSEMOVE} {mouse_x} {mouse_y}'
    #     queue.put(command)

    # elif event == cv2.EVENT_LBUTTONDBLCLK:
    if event == cv2.EVENT_LBUTTONDBLCLK:
        command = f'{EVENT_LBUTTONDBLCLK} {mouse_x} {mouse_y}'
        queue.put(command)

    elif event == cv2.EVENT_LBUTTONDOWN:
        command = f'{EVENT_LBUTTONDOWN} {mouse_x} {mouse_y}'
        queue.put(command)

    elif event == cv2.EVENT_RBUTTONDOWN:
        command = f'{EVENT_RBUTTONDOWN} {mouse_x} {mouse_y}'
        queue.put(command)

    # queue.put(command)
    return


def up():
    print("Go up")


def down():
    print("Go down")


def left():
    print("Go left")


def right():
    print("Go right")


def up_left():
    print("Go up_left")


def up_right():
    print("Go up_right")


def down_left():
    print("Go down_left")


def down_right():
    print("Go down_right")


def do_nothing():
    print("Do Nothing")


combination_to_function = {
    frozenset([Key.up]): up,
    frozenset([Key.down, ]): down,
    frozenset([Key.left, ]): left,
    frozenset([Key.right, ]): right,
    frozenset([Key.up, Key.left]): up_left,
    frozenset([Key.up, Key.right]): up_right,
    frozenset([Key.down, Key.left]): down_left,
    frozenset([Key.down, Key.right]): down_right,
}

current_keys = set()


def on_press(key):
    window = get_active_window_title(CLIENT_OS)
    print(window)

    if WINDOWS_NAME in window:
        print('{0} pressed'.format(key))
        current_keys.add(key)
        if frozenset(current_keys) in combination_to_function:
            combination_to_function[frozenset(current_keys)]()
        else:
            command = f'{EVENT_KB_KEY} {str(key)}'
            queue.put(command)


def on_release(key):
    if key in current_keys:
        current_keys.remove(key)


async def data_channel_client() -> None:
    reader, writer = await asyncio.open_connection(SERVER_HOST, DATA_PORT)
    print('Open data channel')
    while True:
        command = queue.get()
        print(f'Put data channel: {command}')
        writer.write(str(command).encode())
        writer.write(b'\r\n')
        await writer.drain()
        if command == QUIT_COMMAND:
            break
    print('Close data channel...')
    return


async def screen_client() -> None:
    reader, writer = await asyncio.open_connection(SERVER_HOST, SERVER_PORT)
    print('Start screen client')
    num_frames = 0
    listener = Listener(on_press=on_press, on_release=on_release, )
    listener.start()

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
        # cv2.namedWindow(WINDOWS_NAME, flags=cv2.WINDOW_GUI_NORMAL)
        cv2.imshow(WINDOWS_NAME, np.array(img))
        cv2.setMouseCallback(WINDOWS_NAME, on_mouse)

        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            queue.put(QUIT_COMMAND)
            break
        end = time.time()
        seconds = end - start
        fps = num_frames / seconds
        # print("FPS : {0}".format(fps))
    listener.stop()
    return


def start_screen_client():
    loop = asyncio.new_event_loop()
    loop.run_until_complete(screen_client())


def start_data_client():
    loop = asyncio.new_event_loop()
    loop.run_until_complete(data_channel_client())


if __name__ == '__main__':
    screen_thread = threading.Thread(
        target=start_screen_client,
        daemon=True,
    )
    data_thread = threading.Thread(
        target=start_data_client,
        daemon=True,
    )
    screen_thread.start()
    data_thread.start()
    data_thread.join()
    screen_thread.join()

