# Hash Dataserver client
import socket
import sys

#Arguments
ip = sys.argv[1]
port = int(sys.argv[2])

#Connect
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = (ip, port)
sock.connect(address)

#Variables
outData = ""
inData = ""

print("Connection successful.")
print("Usage:")
print("send <message>")
print("   -> returns checksum")
print("request <checksum>")
print("   -> returns message or error")

#Answers
while True:
    inLine = input('> ').split(" ")
    if inLine[0] == "send":
        outData = "#" + inLine[1]
        sock.sendall(outData.encode('UTF-8'))
        inData = sock.recv(1024)
        print(inData.decode('UTF-8'))
    elif inLine[0] == "request":
        outData = "&" + inLine[1]
        sock.sendall(outData.encode('UTF-8'))
        inData = sock.recv(1024)
        print(inData.decode('UTF-8'))
    elif inLine[0] == "exit":
        break
    else:
        print("Invalid.")
        
sock.close()