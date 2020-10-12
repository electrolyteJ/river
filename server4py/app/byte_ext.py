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


def read_int32(buf: bytes):
    v = read32be(buf)
    first = v >> 63
    if first == 1:  # 负数
        v = (v - 1) ^ 0xffffffff
        return int(-v)
    else:
        return v


def read64be(buf: bytes):
    msb = read32be(buf)
    lsb = read32be(buf[4:])
    return (msb << 32) | lsb


def read_int64(buf: bytes):
    '''
    java long 存储有符号数据
    encoding:-1，求补码
    1.1的二进制数
     0x00 00 00 00 00 00 00 01
    2. 取其反码
     0xff ff ff ff ff ff ff fe
    3. 反码+1
     0xff ff ff ff ff ff ff ff  18446744073709551615

     decoding
     1.判读第一位是1,说明是补码，是负数
     2. -1获取反码
     3. 取反
    '''
    msb = read32be(buf)
    lsb = read32be(buf[4:])
    v = (msb << 32) | lsb
    first = v >> 63
    if first == 1:  # 负数
        v = (v - 1) ^ 0xffffffffffffffff
        return int(-v)
    else:
        return v
    # if pow(-2, 63) <= n <= pow(2, 63) - 1:
#     print('cad')


if __name__ == "__main__":
    v = read_int64(bytes(b'\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00'))
    print(
        v,
        type(v)
    )
