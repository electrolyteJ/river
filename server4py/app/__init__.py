from enum import Enum, unique


@unique
class PacketType(Enum):
    METADATA = 0
    AUDIO = 1
    video = 2


class Packet:
    # TimeStamp  uint32 // dts
    # StreamID   uint32
    # Header     PacketHeader
    type: PacketType
    flags: int
    pts: int
    datas: bytes
