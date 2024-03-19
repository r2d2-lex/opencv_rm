import asyncio
import pickle

from mss import mss

mon = {'left': 160, 'top': 160, 'width': 1024, 'height': 768}


HOST = '127.0.0.1'
PORT = 15577
data = None


async def handle_echo(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    addr, port = writer.get_extra_info('peername')
    print(f'Connection from {addr}:{port}')

    with mss() as sct:
        while data != b'quit':

            img = sct.grab(mon)
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


async def run_server() -> None:
    server = await asyncio.start_server(handle_echo, HOST, PORT)
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    print('Start server...')
    loop = asyncio.new_event_loop()
    loop.run_until_complete(run_server())
