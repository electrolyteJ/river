
import asyncio
from aiohttp import web
import subprocess


async def handle_echo(reader, writer):
    while True:
        byte_buffer = await reader.read(1024)
        if byte_buffer is None or len(byte_buffer) == 0:
            continue
        if hex(byte_buffer[0]) == 0x00  \
                and hex(byte_buffer[1]) == 0x00\
                and hex(byte_buffer[2]) == 0x00\
                and hex(byte_buffer[3]) == 0x01:
            print('start code')
        # print("1")
        # await asyncio.sleep(2)
        # print(buffer)
        # print("Received: %d" % b.hex())
        # writer.write(data)
        # await writer.drain()

        # print("Close the connection")
        # writer.close()


async def main():
    subprocess.run('adb reverse --remove-all', shell=True)
    subprocess.run('adb reverse  localabstract:river tcp:27184', shell=True)
    server = await asyncio.start_server(
        handle_echo, '127.0.0.1', 27184)
    print(f'{server.sockets}')
    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

asyncio.run(main())
