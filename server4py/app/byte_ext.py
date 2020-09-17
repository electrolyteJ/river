def copy(src: bytes, dest: bytearray, offset: int = 0):
    src_size = len(src)
    dest_size = len(dest)
    if src_size > dest_size:
        raise BaseException("dest size must be greater than src size")
    for i in range(0, src_size):
        if offset + i >= dest_size:
            break
        dest[offset + i] = src[i]


def read16be(buf):
    return (buf[0] << 8) | buf[1]


def read32be(buf):
    return (buf[0] << 24) | (buf[1] << 16) | (buf[2] << 8) | buf[3]


def read64be(buf: bytes):
    msb = read32be(buf)
    lsb = read32be(buf[4:])
    return (msb << 32) | lsb
