import asyncio, pickle

from mss import mss
from PIL import Image

mon = {'left': 160, 'top': 160, 'width': 1024, 'height': 768}


HOST = '127.0.0.1'
PORT = 15577


async def handle_echo(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    data = None

    with mss() as sct:
        while data != b'quit':

            print('Start')
            screenShot = sct.grab(mon)
            img = Image.frombytes(
                'RGB',
                (screenShot.width, screenShot.height),
                screenShot.rgb,
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
            print('Send end...')
            # input('Y')

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
