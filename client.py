import asyncio
import pickle
import numpy as np
import cv2
import time

from server2 import HOST, PORT

CHUNK = 65536


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

        cv2.imshow('test', np.array(img))
        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            break
        end = time.time()
        seconds = end - start
        fps = num_frames / seconds
        print("FPS : {0}".format(fps))
    return


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(run_client())
