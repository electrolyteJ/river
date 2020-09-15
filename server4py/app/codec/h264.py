from enum import Enum, unique

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
    # unspecified = 0
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
class SliceType(Enum):
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


nalu_non_idr_header = bytes([0x0, 0x0, 0x0, 0x1, 0x41, ])
nalu_idr_header = bytes([0x0, 0x0, 0x0, 0x1, 0x65, ])
nalu_aud_packet = bytes([0x0, 0x0, 0x0, 0x1, 0x09, 0xf0, ])
nalu_sps_header = bytes([0x0, 0x0, 0x0, 0x1, 0x67, ])
nalu_pps_header = bytes([0x0, 0x0, 0x0, 0x1, 0x68, ])


def parse_nalu_type(b: int) -> NaluType:
    return NaluType(b & 0x1f)


def parse_slice_type(b: int) -> SliceType:
    return SliceType((b & 0x60) >> 5)

# def parse_f(b: int) -> NaluType:
#     return NaluType((b & 0x80) >> 5)
