# Import socket module
import socket

# Create a socket object
s = socket.socket()

# Define the port on which you want to connect
port = 80

# connect to the server on local computer
# s.connect(('127.0.0.1', port))
s.connect(('10.15.198.58', port))
s.send('cccc'.encode())
# receive data from the server
print(s.recv(1024))
# close the connection
s.close()
