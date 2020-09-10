
import asyncio
from aiohttp import web
import subprocess


class Packet:
    # isAudio -> bool
    # isVideo -> bool
    # IsMetadata bool
    # TimeStamp  uint32 // dts
    # StreamID   uint32
    # Header     PacketHeader
    flags = 0
    pts = -1
    datas = []


META_HEADER_SIZE = 12
NALU_BYTES_SIZE = 12
NO_PTS = -1

''' The video stream contains raw packets, without time information. When we
     record, we retrieve the timestamps separately, from a "meta" header
     added by the server before each raw packet.
     The "meta" header length is 12 bytes:
     [. . . . . . . .|. . . .]. . . . . . . . . . . . . . . ...
      <-------------> <-----> <-----------------------------...
            PTS        packet        raw packet
                        size

     It is followed by <packet_size> bytes containing the packet/frame.
'''


def read16be(buf):
    return (buf[0] << 8) | buf[1]


def read32be(buf):
    return (buf[0] << 24) | (buf[1] << 16) | (buf[2] << 8) | buf[3]


def read64be(buf):
    msb = read32be(buf)
    lsb = read32be(buf[4:])
    return (msb << 32) | lsb


def byte_to_hexInt(v: int):
    return int(hex(v))


def byte_to_hexStr(v: int):
    return hex(v)


async def handle_echo(reader, writer):
    while True:
        meta_header_buffer = await reader.read(META_HEADER_SIZE)
        pts = int(read64be(meta_header_buffer))
        packet_size = int(read32be(meta_header_buffer[8:]))
        # if pts == NO_PTS or (pts & 0x8000000000000000) == 0 or packet_size <= 0:
        #     continue
        byte_buffer = await reader.read(packet_size)
        # print('cjf:', pts, packet_size)
        # print('cjf:', hex(byte_buffer[0]), hex(byte_buffer[1]), hex(byte_buffer[2]), hex(byte_buffer[3]), hex(byte_buffer[4]))
        if pts <= 0:
            with open('cjf.txt', 'w') as f:
                f.write(str(pts))
                f.write('\t')
                f.write(str(packet_size))
                f.write('\n')
                f.write(str(byte_buffer.hex()))
                f.write('\n')
        if byte_buffer is None or len(byte_buffer) < 3:
            continue
        print('c', type(hex(byte_buffer[0])))
        if hex(byte_buffer[0]) == 0x0:
            print('cadfa')
        if hex(byte_buffer[0]) == 0x0 \
                and hex(byte_buffer[1]) == 0x0\
                and hex(byte_buffer[2]) == 0x0\
                and hex(byte_buffer[3]) == 0x1:
            nalu_type = byte_buffer[4].hex() & 0x1f
            print('start code', nalu_type)

        # writer.write(data)
        # await writer.drain()

        # print("Close the connection")
        # writer.close()
        await asyncio.sleep(2)


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
