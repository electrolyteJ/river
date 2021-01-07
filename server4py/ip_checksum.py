import struct
'''
发送者
'''
# data = "45 00 00 30 80 4c 40 00 80 06 00 00 d3 43 11 7b cb 51 15 3d"
# 45000034d6af4000800600007f0000017f00000122b9fc1f1c7943f85aad34578012ffff688b00000204ffd70103030801010402
data = '''45 00
 00 34
  d6 ae
   40 00
    80 06
     26 13
      7f 00
       00 01
        7f 00
         00 01

          fc 1f
           22 b9
            5a ad 
            34 56 
            00 00 
            00 00 
            80 02 
            ff ff 
            c9 0d 
            00 00 

            02 04 ff d7 01 03 03 08 01 01 04 02'''

def checksum(msg):
    sum=0
    for i in range(0, 20, 2):
        e = (msg[i] <<8 ) | msg[i+1]
        sum += e
    while (sum >> 16 > 0) :
        sum = (sum & 0xFFFF) + (sum >> 16)
    return (0xffff-sum)


def carry_around_add(a, b):
    c = a + b
    return (c & 0xffff) + (c >> 16)


def checksum3(msg):
    s = 0
    for i in range(0, len(msg), 2):
        w = msg[i] + msg[i+1] << 8
        s = carry_around_add(s, w)
    return ~s & 0xffff

data = data.split()
data = [int(x, 16) for x in data ]
data = struct.pack("%dB" % len(data), *data)

print(' '.join(('%02X' % x for x in data)))
print("发送者 Checksum: 0x%04x" % checksum(data))
# print("发送者 Checksum3: 0x%04x" % checksum3(data))


'''
接受者
'''
data2 = '45 00 00 30 80 4c 40 00 80 06 b5 2e d3 43 11 7b cb 51 15 3d'
data2 = data2.split()
data2 = [int(x, 16) for x in data2]
data2 = struct.pack("%dB" % len(data2), *data2)
def checksum_r(msg):
    for i in range(0, 20, 2):
        e = (msg[i] << 8) | msg[i+1]
        checksum += e


print(' '.join(('%02X' % x for x in data2)))
print("接受者 Checksum: 0x%04x" % checksum(data2))
# print("接受者 Checksum3: 0x%04x" % checksum3(data2))
