# Checksum Server

import sys
import socket
import select

# Get args
ip = sys.argv[1]
port = int(sys.argv[2])

# Start server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((ip, port))
sock.listen(1)
socks = [sock]
instance = dict()

# Listen for inputs
while True:
	read, write, exc = select.select(socks, [], [])
	for r in read:
		if r is sock:
			con, addr = r.accept()
			socks.append(con)
		else:
			data = r.recv(1024).decode('UTF-8').split('|')
			if data[0] == "IN":
				fileId = data[1]
				time = data[2]
				length = data[3]
				crc = data[4]
				instance[fileId] = [crc, time]
			elif data[0] == "OUT":
				fileId = data[1]
				con.sendall(str(instance[fileId][0]).encode('UTF-8'))
				del instance[fileId]
