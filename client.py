import asyncio, pickle
import numpy as np
import cv2

from server2 import HOST, PORT

CHUNK = 65536


async def run_client() -> None:
    reader, writer = await asyncio.open_connection(HOST, PORT)

    index = 0
    while True:
        index += 1
        print(f'Index: {index}')

        try:
            packet = await reader.readline()
        except ValueError:
            # separator exception
            print('Cant read size of object')
            continue

        size_of_image = int(packet.decode().rstrip())
        print(f'Data size: {size_of_image}')
        # input('Press Y!')

        data = b''
        loaded_size = size_of_image
        while True:
            print(f'Start read {loaded_size}')

            if loaded_size > CHUNK:
                print('Read chunk')
                data_part = await reader.read(CHUNK)
            else:
                print('Read size')
                data_part = await reader.read(loaded_size)

            if not data_part:
                print('Break')
                break
            loaded_size = loaded_size - len(data_part)
            data += data_part
            data_size = len(data)
            print(f'Data_size: {data_size} size_of_image: {size_of_image} loaded size: {loaded_size}\r\n')
            if data_size >= size_of_image:
                print(f'All data will downloaded...')
                break
            if not loaded_size:
                break

        print(f'Start loads...')
        img = pickle.loads(data)

        cv2.imshow('test', np.array(img))
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            break
        print('Return...')
    return


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(run_client())
