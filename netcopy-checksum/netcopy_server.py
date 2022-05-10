# Netcopy Server
import sys
import socket
import zlib

# Get args
ip = sys.argv[1]
port = int(sys.argv[2])
checkIp = sys.argv[3]
checkPort = int(sys.argv[4])
fileId = sys.argv[5]
filePath = sys.argv[6]

# Start server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = (ip, port)
sock.bind(address)
sock.listen(1)

connection, clientAddress = sock.accept()
data = connection.recv(1024)

# Receieve data
text = ""
while data != "end":
	text += str(data)
	data = connection.recv(1024).decode('UTF-8')
	with open(filePath, 'w') as file:
		file.write(text)
	file.close()
connection.close()

# Verify checksum
crc = hex(zlib.crc32((text).encode('UTF-8')) % (1 << 32))
crcLength = len(crc)

# Send answer
answerConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
answerConnection.connect((checkIp, checkPort))
answerConnection.sendall(("OUT|" + fileId).encode('UTF-8'))

# Verify answer
checksum = answerConnection.recv(crcLength)
verification = answerConnection.recv(1024).data.decode().split('|')

if verification[0] == 0 or verification[1] != checksum:
	print("Checksum Corrupted!")
else:
	print("Checksum OK!")

answerConnection.close()