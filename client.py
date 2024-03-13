import asyncio
import time

HOST = '127.0.0.1'
PORT = 15577


async def run_client() -> None:
    reader, writer = await asyncio.open_connection(HOST, PORT)
    writer.write(b'Hello world!')
    await writer.drain()

    while True:
        data = await reader.read(1024)

        if not data:
            raise Exception('Socket closed')

        print(f'Received: {data.decode()!r}')


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(run_client())
