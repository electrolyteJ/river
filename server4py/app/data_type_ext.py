'''
python 基本数据类型：
- 
'''
import math


def int8(n):
    pass


def uint8(n):
    return int(n) & 0xff


def int16(n: int) -> int:
    pass


def uint16(n: int) -> int:
    return int(n) & 0xffff


def int32(n: int) -> int:
    """
     [−(2 ^31), (2^31) − 1]
    :param n:
    :return :如果参数n的值在有符号整形区间则不做处理，如果参数n的值在区间右边则参数n抹去最后一位，去剩余七位的值，在区间右边同理。
    """
    if math.pow(-2, 31) <= n <= math.pow(2, 31) - 1:
        return n
    elif n > math.pow(2, 31) - 1:
        return uint32(n) >> 1
    elif n < math.pow(-2, 31):
        return -(uint32(n) >> 1)


def uint32(n: int) -> int:
    return int(n) & 0xffffffff


def int64(n: int):
    """
    [−(2 ^63), (2^63) − 1]
    """
    if math.pow(-2, 63) <= n <= math.pow(2, 63) - 1:
        return n
    elif n > math.pow(2, 63) - 1:
        return uint64(n) >> 1
    elif n < math.pow(-2, 63):
        return -(uint64(n) >> 1)


def uint64(n: int) -> int:
    return n & 0xffffffffffffffff


def byte(n: int) -> int:
    """
     [−(2 ^7), (2^7) − 1]
    """
    if math.pow(-2, 7) <= n <= math.pow(2, 7) - 1:
        return n
    elif n > math.pow(2, 7) - 1:
        return ubyte(n) >> 1
    elif n < math.pow(-2, 7):
        return -(ubyte(n) >> 1)


def ubyte(n: int) -> int:
    return n & 0xff

if __name__ == "__main__":
    print(int32(2147483648))
