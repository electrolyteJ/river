from enum import Enum, unique
from typing import Optional
from asyncio.streams import StreamReader

'''
                     4bytes          1bytes              
  +-+-+-+-+-+-+    +-+-+-+-+-+-+-+-++-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
  |NALU/Packet| =  | start code | Packet header |       Packet data       |
  +-+-+-+-+-+-+    +-+-+-+-+-+-+-+-++-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
  
  
 0 1 2 3 4 5 6 7
+-+-+-+-+-+-+-+-+
|F|NRI|   Type  |          
+-+-+-+-+-+-+-+-+
F:   占1bit,forbidden_zero_bit，h.264规定必须取0，禁止位，当网络发现NAL单元有比特错误时可设置该比特为1，以便接收方纠错或丢掉该单元。
NRI: 占2bit,nal_ref_idc，取值0~3，指示这个nalu的重要性，I帧、sps、pps通常取3，P帧通常取2，B帧通常取0，nal重要性指示，标志该NAL单元的重要性，值越大，越重要，解码器在解码处理不过来的时候，可以丢掉重要性为0的NALU。


Type:占5bit, nal_unit_type:0=未使用 1=非IDR图像片，IDR指关键帧
                           2=片分区A 3=片分区B
                           4=片分区C 5=IDR图像片，即关键帧
                           6=补充增强信息单元(SEI) 7=SPS序列参数集
                           8=PPS图像参数集 9=分解符
                           10=序列结束 11=码流结束
                           12=填充
                           13~23=保留 24~31=未使用
'''


@unique
class NaluType(Enum):
    """
    0      Unspecified                                                    non-VCL
    1      Coded slice of a non-IDR picture                               VCL
    2      Coded slice data partition A                                   VCL
    3      Coded slice data partition B                                   VCL
    4      Coded slice data partition C                                   VCL
    5      Coded slice of an IDR picture                                  VCL
    6      Supplemental enhancement information (SEI)                     non-VCL
    7      Sequence parameter set                                         non-VCL
    8      Picture parameter set                                          non-VCL
    9      Access unit delimiter                                          non-VCL
    10     End of sequence                                                non-VCL
    11     End of stream                                                  non-VCL
    12     Filler data                                                    non-VCL
    13     Sequence parameter set extension                               non-VCL
    14     Prefix NAL unit                                                non-VCL
    15     Subset sequence parameter set                                  non-VCL
    16     Depth parameter set                                            non-VCL
    17..18 Reserved                                                       non-VCL
    19     Coded slice of an auxiliary coded picture without partitioning non-VCL
    20     Coded slice extension                                          non-VCL
    21     Coded slice extension for depth view components                non-VCL
    22..23 Reserved                                                       non-VCL
    24..31 Unspecified                                                    non-VCL
"""
    UNSPECIFIED = 0
    SLICE_NONIDR = 1
    SLICE_PA = 2
    SLICE_PB = 3
    SLICE_PC = 4
    SLICE_IDR = 5  # 关键帧 keyframe
    SEI = 6
    SPS = 7
    PPS = 8
    AUD = 9
    END_OF_SEQUENCE = 10
    END_Of_STREAM = 11
    FILLER_DATA = 12


@unique
class FrameType(Enum):
    UNKNOWN = -1
    B = 0
    P = 2
    I = 3
    # SP = 3
    # SI = 4
    # P = 5
    # B = 6
    # I = 7
    # SP = 8
    # IS = 9


NALU_START_CODE = bytes([0x00, 0x00, 0x00, 0x01])
NALU_START_CODE_SIZE = 4
NALU_NON_IDR_HEADER = bytes([0x0, 0x0, 0x0, 0x1, 0x41, ])
NALU_IDR_HEADER = bytes([0x0, 0x0, 0x0, 0x1, 0x65, ])
NALU_AUD_PACKET = bytes([0x0, 0x0, 0x0, 0x1, 0x09, 0xf0, ])
NALU_SPS_HEADER = bytes([0x0, 0x0, 0x0, 0x1, 0x67, ])
NALU_PPS_HEADER = bytes([0x0, 0x0, 0x0, 0x1, 0x68, ])

# def parse_f(b: int) -> NaluType:
#     return NaluType((b & 0x80) >> 5)

PACKET_TYPE_METADATA = 0
PACKET_TYPE_AUDIO = 1
PACKET_TYPE_VIDEO = 2


class Header:
    pts: int = 0  # unit:millisecond
    dts: int = 0
    frame_type: FrameType = FrameType.UNKNOWN
    nalu_type: NaluType = NaluType.UNSPECIFIED
    type: int = -1
    __flags: int = 0
    payload_size: int = 0

    def is_keyframe(self):
        return self.frame_type == FrameType.I

    def is_sps(self):
        return self.nalu_type == NaluType.SPS

    def is_metadata_packet(self):
        return self.type == PACKET_TYPE_METADATA

    def is_audio_packet(self):
        return self.type == PACKET_TYPE_AUDIO

    def is_video_packet(self):
        return self.type == PACKET_TYPE_VIDEO


class Frame:
    """
     type:I Frame, P Frame , B Frame
    """

    def __init__(self, header: Header, payload: bytes) -> None:
        super().__init__()
        self.header = header
        self.payload = payload


class Parser:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__reader.close()

    def __init__(self, path: str = None, sr: StreamReader = None) -> None:
        if path is None and sr is None or (path and sr):
            raise BaseException('path and StreamReader must exit one of tow')
        super().__init__()

        self.__reader = open(path, 'r') if path else sr

        l0 = self.__reader.readline()
        self.__sps_pps = self.__reader.readline().strip()

    def __fill_data(self, buffer, rr):
        for e in rr:
            if len(e) == 0:
                continue
            buffer.append(int(e.strip(), base=16))

    def __parse_nalu_type(self, b: int) -> NaluType:
        return NaluType(b & 0x1f)

    def __parse_frame_type(self, b: int) -> FrameType:
        return FrameType((b & 0x60) >> 5)

    def __parse_frame(self, metadata, p) -> Frame:
        ret = p.strip().split(',')
        nt = self.__parse_nalu_type(int(ret[4], base=16))
        ft = self.__parse_frame_type(int(ret[4], base=16))

        header = Header()
        pts, packet_size = metadata.strip().split("\t")
        g_pts = int(pts)  # microsecond
        header.dts = int(g_pts / 1000)  # millisecond
        header.pts = int(g_pts / 1000)  # millisecond
        header.type = PACKET_TYPE_VIDEO
        header.payload_size = int(packet_size)
        header.nalu_type = nt
        header.frame_type = ft
        es = bytearray()
        # if nt != NaluType.SLICE_IDR:
        es.extend(NALU_AUD_PACKET)
        self.__fill_data(es, ret)
        return Frame(header, es)

    def next_frame(self) -> Optional[Frame]:
        reader = self.__reader
        header = reader.readline()
        frame = reader.readline()
        if len(frame) != 0:
            ret = frame.strip().split(',')
            if self.__parse_frame_type(int(ret[4], base=16)) == FrameType.I:
                frame = self.__sps_pps + ',' + frame
            return self.__parse_frame(header, frame) if len(frame) != 0 else None
        else:
            return None
