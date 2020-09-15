from unittest import TestCase
from app.container.ts import ts_pes_packet, pat_packet, pmt_packet
# from container import datas
from app.container import print_ts_packet
from app import Packet, Packet_Type_VIDEO, Packet_Type_AUDIO
import os
import time
from app.codec.h264 import nalu_aud_packet, NaluType, SliceType
from app.data_type_ext import int32, uint64, uint32
import math
from app.codec import h264


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
        def fill_data(buffer, rr):
            for e in rr:
                if len(e) == 0:
                    continue
                buffer.append(int(e.strip(), base=16))

        ps = list()
        with open('v_datas1.txt', 'r') as f:
            r = f.readline()
            es = bytearray()
            g_packet_size = 0
            g_pts = 0
            header = dict()
            compositionTime = 0
            ii = 0
            g_pre_pts = 0
            while len(r) != 0:
                if '0x' in r:
                    rr = r.strip().split(',')

                    nt = h264.parse_nalu_type(int(rr[4], base=16))
                    st = h264.parse_slice_type(int(rr[4], base=16))
                    # print(ii, 'nalu_type:%s,slice_type:%s' % (nt, st))
                    ii += 1

                    if nt == NaluType.SPS:
                        g_pre_pts = g_pts
                        es.extend(nalu_aud_packet)
                        fill_data(es, rr)
                    elif nt == NaluType.SLICE_IDR and st == SliceType.I:
                        header['is_keyframe'] = True
                        # header['dts'] = g_pts - g_pre_pts if g_pts - g_pre_pts > 0 else 0
                        # header['pts'] = g_pts - g_pre_pts if g_pts - g_pre_pts > 0 else 0
                        # g_pre_pts = g_pts
                        fill_data(es, rr)
                        ps.append(Packet(header.copy(), es[0:]))
                        es.clear()
                        g_packet_size = 0
                    elif st == SliceType.P:
                        # header['dts'] = g_pts - g_pre_pts if g_pts - g_pre_pts > 0 else 0
                        # header['pts'] = g_pts - g_pre_pts if g_pts - g_pre_pts > 0 else 0
                        # g_pre_pts = g_pts
                        header['is_keyframe'] = False
                        es.extend(nalu_aud_packet)
                        fill_data(es, rr)
                        ps.append(Packet(header.copy(), es[0:]))
                        es.clear()
                        g_packet_size = 0

                    # if nt == NaluType.SLICE_NONIDR:
                    #     print('NaluType.NONIDR')
                    # elif nt == NaluType.SLICE_IDR:
                    #     for i in range(6, 6 + 3):
                    #         compositionTime = int32(compositionTime << 8) + int(rr[i], base=16)
                    #     print('NaluType.IDR')
                    # elif nt == NaluType.SPS:
                    #     print('NaluType.SPS')
                    # elif nt == NaluType.AUD:
                    #     print('NaluType.AUD')

                else:
                    pts, packet_size = r.strip().split("\t")
                    g_packet_size += int(packet_size)
                    g_pts = int(pts)  # microsecond
                    header['dts'] = int(g_pts / 1000) * 90  # millisecond
                    header['pts'] = int(g_pts / 1000) * 90  # millisecond
                    # 1s = 90000 time scale , 一帧就应该是  90000/video_frame_rate 个timescale
                    video_frame_rate = 60
                    video_bit_rate = 8
                    video_pts_increment = uint32(90000 / video_frame_rate)

                    header['type'] = Packet_Type_VIDEO
                    header['payload_size'] = g_packet_size

                r = f.readline()

        print("=" * 20)
        print('split elematry stream into %d size' % len(ps))
        with open('001.ts', 'w') as f:
            f.write('')
        with open('001.ts', 'ab') as f:
            # f.truncate(0)
            ps_size = len(ps)
            for i in range(0, ps_size):
                p = ps[i]
                is_video = True if p.header['type'] == Packet_Type_VIDEO else False

                print('%d dts:%d , pts:%d,is_keyframe:%s,is_video:%s,es packet size:%d' % (
                    i, p.header['dts'], p.header['pts'], p.header['is_keyframe'], is_video, len(p.payload)))

                ts_pes_packets_size, ts_pes_packets = ts_pes_packet(
                    p.payload,
                    is_video,
                    p.header['is_keyframe'],
                    p.header['pts'], p.header['dts']
                )
                f.write(pat_packet())
                f.write(pmt_packet(is_video))
                for ts_packet in ts_pes_packets:
                    f.write(ts_packet)
