# first of all import the socket library
import socket
import subprocess
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

    # send a thank you message to the client.
    # c.send("Thank you for connecting".encode())
    buffer = c.recv(1024)
    if buffer is not None and len(buffer) > 0:
        print(hex(buffer[0]), hex(buffer[1]), hex(buffer[2]), hex(buffer[3]))
    else:
        pass
    # Close the connection with the client

c.close()
