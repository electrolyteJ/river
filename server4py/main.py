from util import *
import asyncio
from aiohttp import web
import subprocess
from codec.h264 import NaluType


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
NALU_BYTES_SIZE = 4
START_CODE_SIZE = 4
start_code = bytes([0x00, 0x00, 0x00, 0x01])
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


async def handle_echo(reader, writer):
    while True:
        # java long:ff ff ff ff ff ff ff ff -2^63 ~ 2^63
        # java int:00 00 00 20
        meta_header_buffer = await reader.read(META_HEADER_SIZE)
        if meta_header_buffer is None or len(meta_header_buffer) == 0:
            continue
        print('meta_header_buffer', meta_header_buffer.hex())
        pts = read64be(meta_header_buffer)
        packet_size = read32be(meta_header_buffer[8:])
        byte_buffer = await reader.read(packet_size)
        if byte_buffer is None or len(byte_buffer) < 3:
            continue
        sc = byte_buffer[:START_CODE_SIZE]
        nalu_header = byte_buffer[START_CODE_SIZE]
        nalu_payload_buffer = byte_buffer[START_CODE_SIZE + 1:]
        # if pts == NO_PTS or (pts & 0x8000000000000000) == 0 or packet_size <= 0:
        #     continue
        print('cjf pts/packet_size:', pts, packet_size)
        s = ''
        for i in range(0, len(byte_buffer)):
            p = byte_buffer[i]
            if len(s) == 0:
                s = hex(p)
            else:
                s = s + ',' + hex(p)
        with open('cjf.txt', 'a') as f:
            f.write(str(pts))
            f.write('\t')
            f.write(str(packet_size))
            f.write('\n')
            f.write(s)
            f.write('\n')
        if sc == start_code:
            nalu_type = nalu_header & 0x1f
            print('start code nalu_type', nalu_type)
            if nalu_type == NaluType.SLICE_NONIDR.value:
                # print('NaluType.NONIDR')
                pass
            elif nalu_type == NaluType.SLICE_IDR.value:
                print('NaluType.IDR')
            elif nalu_type == NaluType.SPS.value:
                print('NaluType.SPS')
            elif nalu_type == NaluType.AUD.value:
                print('NaluType.AUD')

                # writer.write(data)
                # await writer.drain()

                # print("Close the connection")
                # writer.close()
                # await asyncio.sleep(2)


async def main():
    # meta_header_buffer = [0, 13024]
    # pts = read64be(meta_header_buffer)
    # print(pts)
    subprocess.run('adb reverse --remove-all', shell=True)
    subprocess.run('adb reverse  localabstract:river tcp:27184', shell=True)
    server = await asyncio.start_server(
        handle_echo, '127.0.0.1', 27184)
    print(f'{server.sockets}')
    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())
