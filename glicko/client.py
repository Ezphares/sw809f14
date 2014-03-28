import sys
import socket
import json

(host, port) = 'localhost', 9999
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

id = int(sys.argv[1])
rating = int(sys.argv[2])
rd = int(sys.argv[3])

try:
	sock.connect((host, port))
	json = json.dumps({'id': id, 'rating': rating, 'rd': rd})
	sock.sendall(json.encode('utf-8'))
finally:
	sock.close()
