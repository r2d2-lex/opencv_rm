import asyncio
import pickle
import threading

from mss import mss
from utils import get_monitor_resolution
from config import SERVER_HOST, SERVER_PORT, DATA_PORT

# monitor = {'left': 160, 'top': 160, 'width': 1024, 'height': 768}
monitor = {'left': 0, 'top': 0, 'width': 800, 'height': 600}

data = None


async def data_channel(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    addr, port = writer.get_extra_info('peername')
    print(f'Open data channel from {addr}:{port}')
    while True:
        try:
            packet = await reader.readline()
        except ValueError:
            # separator exception
            print('Cant read size of object')
            continue
        command = packet.decode().rstrip()
        print(f'Data channel command: {command}')


async def handle_echo(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    addr, port = writer.get_extra_info('peername')
    print(f'Connection from {addr}:{port}')
    print(f'Capture settings: {monitor}')

    with mss() as sct:
        while data != b'quit':

            img = sct.grab(monitor)
            img_pickled = pickle.dumps(img)
            data_length = len(img_pickled)

            try:
                writer.write(str(data_length).encode())
                writer.write(b'\r\n')
                await writer.drain()

                writer.write(img_pickled)
                await writer.drain()
            except ConnectionResetError as err:
                print(f'{err}')
                break

        try:
            writer.close()
            await writer.wait_closed()
        except ConnectionResetError as err:
            pass
        print('Write closed....')


async def run_server(handle, host, port) -> None:
    server = await asyncio.start_server(handle, host, port)
    async with server:
        await server.serve_forever()


def start_server(handle, host, port):
    loop = asyncio.new_event_loop()
    loop.run_until_complete(run_server(handle, host, port))


if __name__ == '__main__':
    print('Start server...')
    width, height = get_monitor_resolution()
    print(f'Resolution Width: {width} Height {height}')
    # monitor['width'] = width
    # monitor['height'] = height

    screen_thread = threading.Thread(
        target=start_server,
        args=(handle_echo, SERVER_HOST, SERVER_PORT),
        daemon=True,
    )
    data_thread = threading.Thread(
        target=start_server,
        args=(data_channel, SERVER_HOST, DATA_PORT),
        daemon=True,
    )
    screen_thread.start()
    data_thread.start()
    data_thread.join()
    screen_thread.join()
