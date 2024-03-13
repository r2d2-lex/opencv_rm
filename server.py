import asyncio
import socket

import numpy as np
import cv2
from mss import mss
from PIL import Image

bounding_box = {'top': 100, 'left': 100, 'width': 1280, 'height': 960}

sct = mss()


async def handle_client(client):
    loop = asyncio.get_event_loop()
    request = None
    while request != 'quit':
        request = (await loop.sock_recv(client, 255)).decode('utf8')
        response = str(eval(request)) + '\n'
        print(f'response: {response}')
        await loop.sock_sendall(client, response.encode('utf8'))
    client.close()


async def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 15555))
    server.listen(8)
    server.setblocking(False)

    loop = asyncio.get_event_loop()

    while True:
        client, _ = await loop.sock_accept(server)
        loop.create_task(handle_client(client))


def main():
    asyncio.run(run_server())
    print('Test')
    # while True:
    #     sct_img = sct.grab(bounding_box)
    #     cv2.imshow('screen', np.array(sct_img))
    #
    #     if (cv2.waitKey(1) & 0xFF) == ord('q'):
    #         cv2.destroyAllWindows()
    #         break


if __name__ == '__main__':
    main()
