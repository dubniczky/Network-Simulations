# Netcopy Client

import sys
import socket
import zlib

# Constants
ttlSec = 60
endString = "end"

# Get Args
ip = sys.argv[1]
port = int(sys.argv[2])
serverIp = sys.argv[3]
serverPort = int(sys.argv[4])
fileId = sys.argv[5]
filePath = sys.argv[6]

# Connect to server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((ip, port))
serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverAddress = (serverIp, serverPort)

# Read file to send
text = ""
with open(filePath, 'r') as file:
	for chunk in file:
		text += chunk
file.close()

# Verify checksum
crc = hex(zlib.crc32((text).encode('UTF-8')) % (1 << 32))
crcLength = len(crc)

# Send header
serverSock.connect(serverAddress)
data = "IN|" + fileId + "|" + str(ttlSec) + "|" + str(crcLength) + "|" + str(crc)
serverSock.sendall(data.encode('UTF-8'))
serverSock.close()

# Send file
with open(filePath, 'r') as sendFile:
	for chunk in sendFile:
		sock.sendall(chunk.encode('UTF-8'))
	sock.sendall(endString.encode('UTF-8'))

sock.close()