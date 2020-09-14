from unittest import TestCase
from app.container.ts import ts_pes_packet, pat_packet, pmt_packet
# from container import datas
from app.container import print_ts_packet
from app import Packet, Packet_Type_VIDEO


class TestTS_all(TestCase):

    def test_audio_pes_packet(self):
        expected_ret = bytes([
            0x47, 0x41, 0x01, 0x31,
            0x81, 0x00, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff,
            # pes header
            # 0x0, 0x0,  0x1,  0xc0, 0x0, 0x30, 0x80, 0x80, 0x5,  0x21, 0x0,  0x1 ,  0x7, 0xd1
            0x00, 0x00, 0x01, 0xc0, 0x00, 0x30, 0x80, 0x80, 0x05, 0x21, 0x00, 0x01, 0x00, 0x01,
            # pes payload
            0xaf, 0x01, 0x21, 0x19, 0xd3, 0x40, 0x7d, 0x0b, 0x6d, 0x44, 0xae, 0x81, 0x08, 0x00, 0x89, 0xa0, 0x3e,
            0x85, 0xb6, 0x92, 0x57, 0x04, 0x80, 0x00, 0x5b, 0xb7, 0x78, 0x00, 0x84, 0x00, 0x00, 0x00, 0x00, 0x00, 0x38,
            0x30, 0x00, 0x06, 0x00, 0x38])
        __TS_PACKET_SIZE = 188
        is_video = False
        is_keyframe = False
        es_buffer = bytes([0xaf, 0x01, 0x21, 0x19, 0xd3, 0x40, 0x7d, 0x0b, 0x6d, 0x44, 0xae, 0x81,
                           0x08, 0x00, 0x89, 0xa0, 0x3e, 0x85, 0xb6, 0x92, 0x57, 0x04, 0x80, 0x00, 0x5b, 0xb7,
                           0x78, 0x00, 0x84, 0x00, 0x00, 0x00, 0x00, 0x00, 0x38, 0x30, 0x00, 0x06, 0x00, 0x38,
                           ])
        ts_packets_size, ts_packets = ts_pes_packet(es_buffer, is_video, is_keyframe, 0, 0)

        for i in range(0, len(ts_packets)):
            p = ts_packets[i]
            print("=" * 20)
            print('index', i)
            print_ts_packet(p)

    def test_video_pes_packet(self):

        pts = 0
        # with open('v_datas0.txt', 'r') as f:
        #     r = f.readline()
        #
        #     while len(r) != 0:
        #         if "#" in r or ']}' in r:
        #             pass
        #         elif "{'pts'" in r:
        #             end = r.index("'es'") - 1
        #             pts = int(r[7:end])
        #         else:
        #             for e in r.strip().split(','):
        #                 if len(e) == 0:
        #                     continue
        #                 es.append(int(e.strip(), base=16))
        #
        #         r = f.readline()
        ps = list()
        with open('v_datas1.txt', 'r') as f:
            r = f.readline()
            es = bytearray()
            g_packet_size = 0
            is_first = True
            g_pts = 0
            header = dict()
            while len(r) != 0:

                if '0x' in r:

                    if g_packet_size > 60000:
                        header['type'] = Packet_Type_VIDEO
                        header['is_keyframe'] = True if is_first else False
                        print('超出', pts, g_packet_size, len(es))
                        ps.append(Packet(header.copy(), es[0:]))
                        is_first = False
                        g_packet_size = 0
                        es.clear()
                        print(len(es))
                    for e in r.strip().split(','):
                        if len(e) == 0:
                            continue
                        es.append(int(e.strip(), base=16))

                else:
                    pts, packet_size = r.strip().split("\t")
                    g_packet_size += int(packet_size)
                    g_pts = int(pts)
                    header['pts'] = g_pts
                    header['payload_size'] = g_packet_size

                r = f.readline()
            if len(es) > 0:
                print('last packet :es size',len(es))
                header['type'] = Packet_Type_VIDEO
                header['is_keyframe'] = True if is_first else False
                ps.append(Packet(header.copy(), es[0:]))

        # es_size = len(es)
        # if es_size > 65526:
        #     es = es[0:60000]
        print('ps',len(ps))
        for i in range(0, len(ps)):
            p = ps[i]
            is_video = True if p.header['type'] == Packet_Type_VIDEO else False
            print('pts',p.header['pts'],p.header['is_keyframe'],is_video)
            ts_pes_packets_size, ts_pes_packets = ts_pes_packet(
                p.payload,
                is_video,
                p.header['is_keyframe'],
                p.header['pts'], p.header['pts'] - 2
            )
            # print(ts_pes_packets_size)
            # for i in range(0, len(ts_packets)):
            #     p = ts_packets[i]
            #     print("=" * 20)
            #     print('index', i)
            #     print_ts_packet(p)
            with open('00%d.ts' % (i + 1), 'wb') as f:
                f.write(pat_packet())
                f.write(pmt_packet(is_video))
                for ts_packet in ts_pes_packets:
                    f.write(ts_packet)
