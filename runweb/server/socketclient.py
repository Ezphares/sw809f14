import socket
import sys

host = sys.argv[1]
port = int(sys.argv[2])
msg = str.encode(sys.argv[3])

print(host)
print(port)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
s.send(msg)
s.close()
