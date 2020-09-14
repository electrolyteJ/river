from enum import Enum, unique

Packet_Type_METADATA = 0
Packet_Type_AUDIO = 1
Packet_Type_VIDEO = 2


class Packet:
    # TimeStamp  uint32 // dts
    # StreamID   uint32
    # type
    # flags: int
    pts: int

    def __init__(self, header: dict, payload: bytes) -> None:
        """
        :param header: container field pts/dts ,type ,flags,payload_size
        :param payload:
        """
        super().__init__()
        self.header = header
        self.payload = payload
