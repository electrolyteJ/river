def read16be(buf):
    return (buf[0] << 8) | buf[1]


def read32be(buf):
    return (buf[0] << 24) | (buf[1] << 16) | (buf[2] << 8) | buf[3]


def read64be(buf):
    msb = read32be(buf)
    lsb = read32be(buf[4:])
    return (msb << 32) | lsb

