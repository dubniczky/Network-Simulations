# Hash Dataserver server
import socket
import hashlib
import sys

#Arguments
ip = sys.argv[1]
port = int(sys.argv[2])

#Connect
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = (ip, port)
sock.bind(address)

sock.listen(1)

hashes = {}
connection, clientAddress = sock.accept()

#Listen
while True:
    data = connection.recv(1024)
    data = data.decode('UTF-8')
    print("Received:", data)
    response = ""
    if data[0] == '#':
        inString = data[1:]
        response = hashlib.md5(inString.encode()).hexdigest()
        hashes[response] = inString
    if data[0] == '&':
        inString = data[1:]
        if inString in hashes.keys():
            response = "SUCCESS: " +  hashes[inString]
        else:
            response = 'FAILED'
    print("Sent:", response)
    connection.sendall(response.encode('UTF-8'))

connection.close()