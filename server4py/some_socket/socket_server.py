# first of all import the socket library
import socket
import subprocess

import time


def read16be(buf):
    return (buf[0] << 8) | buf[1]


def read32be(buf):
    return (buf[0] << 24) | (buf[1] << 16) | (buf[2] << 8) | buf[3]


def read64be(buf):
    msb = read32be(buf)
    lsb = read32be(buf[4:])
    return (msb << 32) | lsb


subprocess.run('adb reverse --remove-all', shell=True)
subprocess.run('adb reverse  localabstract:river tcp:27184', shell=True)
# next create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket successfully created")

# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 27184

# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network
s.bind(('', port))
print("socket binded to %s" % (port))

# put the socket into listening mode
s.listen(5)
print("socket is listening")
# Establish connection with client.
c, addr = s.accept()
print('Got connection from', addr)

# a forever loop until we interrupt it or
# an error occurs
while True:
    # java long:ff ff ff ff ff ff ff ff -2^63 ~ 2^63
    # java int:00 00 00 20
    meta_header_buffer = c.recv(12)

    if meta_header_buffer is None or len(meta_header_buffer) == 0:
        continue
    # print('meta_header_buffer', meta_header_buffer.hex())
    pts = read64be(meta_header_buffer)
    packet_size = read32be(meta_header_buffer[8:])
    print(pts, packet_size)
    byte_buffer = c.recv(packet_size)
    if byte_buffer is None or len(byte_buffer) < 3:
        continue
    # print(hex(meta_header_buffer[0]), hex(meta_header_buffer[1]), hex(meta_header_buffer[2]), hex(meta_header_buffer[3]))
    # send a thank you message to the client.
    # c.send("Thank you for connecting".encode())
    # Close the connection with the client
    # time.sleep(2)

c.close()
