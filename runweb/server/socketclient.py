import argparse
import socket
import struct


class SocketClient:

	def __init__(self, host, port):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect((host, port))

	def send(self, msg):
		msg = struct.pack('!h', len(msg)) + msg.encode('utf-8')
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
	parser.add_argument('host', help='The host to connect to.')
	parser.add_argument('port', help='The port to use.', type=int)
	parser.add_argument('id', help='The player id to use.')
	valid_cmds = ['queue', 'cancel', 'accept', 'decline', 'position']
	parser.add_argument('cmds', help='The commands to send.', nargs='+', choices=valid_cmds)
	args = parser.parse_args()

	client = SocketClient(args.host, args.port)
	for cmd in args.cmds:
		if cmd == 'queue':
			msg = '{{"cmd": "{0}", "id": {1}, "data": {{"route_id": 1}}}}'.format(cmd, args.id)
		elif cmd == 'position':
			msg = '{{"cmd": "{0}", "id": {1}, "data": {{"lat": 10.0, "lng": 10.0}}}}'.format(cmd, args.id)
		else:
			msg = '{{"cmd": "{0}", "id": {1}, "data": null}}'.format(cmd, args.id)
		print(msg)
		client.send(msg)
		header = client.recv_n(2, False)
		msg_len = struct.unpack('!h', header)[0]
		print(client.recv_n(msg_len))
	client.socket.shutdown(socket.SHUT_RDWR)
	client.socket.close()

if __name__ == "__main__":
    main()
