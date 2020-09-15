import math


def int8(n):
    pass


def uint8(n):
    pass


def int16(n):
    pass


def uint16(n):
    pass


def int32(n):
    """
     [−(2 ^31), (2^31) − 1]
    :param n:
    :return:
    """
    if math.pow(-2, 31) <= n <= math.pow(2, 31) - 1:
        return n
    elif n > math.pow(2, 31) - 1:
        return uint32(n) >> 1
    elif n < math.pow(-2, 31):
        return -(uint32(n) >> 1)


def uint32(n):
    return int(n) & 0xffffffff


def int64(n):
    pass


def uint64(n):
    return n & 0xffffffffffffffff


def byte(n):
    return n & 0xff
