import argparse
import socket
import struct


class SocketClient:

	def __init__(self, host, port):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect((host, port))

	def send(self, msg):
		msg = struct.pack('<I', len(msg)) + msg.encode('utf-8')
		totalsent = 0
		while totalsent < len(msg):
			sent = self.socket.send(msg[totalsent:])
			if sent == 0:
				raise RuntimeError("Error while sending.")
			totalsent += sent

	def recv_n(self, n, decode=True):
		data = b''
		while len(data) < n:
			chunk = self.socket.recv(n - len(data))
			if chunk == b'':
				raise RuntimeError("Error while receiving.")
			data += chunk
		if decode:
			return data.decode('utf-8')
		return data


def main():
	parser = argparse.ArgumentParser(description='A simple socket client implementation for testing purposes.')
	parser.add_argument("host", help="The host to connect to.")
	parser.add_argument("port", help="The port to use.", type=int)
	parser.add_argument("msg", help="The message to send.")
	args = parser.parse_args()

	client = SocketClient(args.host, args.port)
	client.send(args.msg)
	header = client.recv_n(4, False)
	msg_len = struct.unpack('<I', header)[0]
	print(client.recv_n(msg_len))

if __name__ == "__main__":
    main()
