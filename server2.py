import asyncio
import pickle

from mss import mss
from PIL import Image

mon = {'left': 160, 'top': 160, 'width': 1024, 'height': 768}


HOST = '127.0.0.1'
PORT = 15577


async def handle_echo(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    data = None

    with mss() as sct:
        while data != b'quit':

            screen_shot = sct.grab(mon)
            img = Image.frombytes(
                'RGB',
                (screen_shot.width, screen_shot.height),
                screen_shot.rgb,
            )

            addr, port = writer.get_extra_info('peername')
            print(f'Connection from {addr}:{port}')

            img_pickled = pickle.dumps(img)
            data_length = len(img_pickled)
            print(f'data_length: {data_length}')
            writer.write(str(data_length).encode())
            writer.write(b'\r\n')
            await writer.drain()

            writer.write(img_pickled)
            await writer.drain()

        print('Write closed....')
        writer.close()
        await writer.wait_closed()


async def run_server() -> None:
    server = await asyncio.start_server(handle_echo, HOST, PORT)
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(run_server())
