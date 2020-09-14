from enum import Enum, unique


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
    P = 0
    B = 1
    I = 2
    SP = 3
    SI = 4
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


def parse():
    pass
