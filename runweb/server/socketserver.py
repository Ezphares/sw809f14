import json
import logging
import queue
import socket
import struct
import threading

from server.matchmaker import Matchmaker


class SocketServer:

	def __init__(self, host, port):
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.bind((host, port))
		self.server.listen(socket.SOMAXCONN)
		logging.info('Server listening on ' + str((host, port)))

		self.matchmaking_q = queue.Queue()
		self.reply_q = {}

		matchmaker = Matchmaker(self.matchmaking_q, self.reply_q)
		threading.Thread(target=matchmaker.run).start()

	def run(self):
		while True:
			(clientsocket, address) = self.server.accept()
			logging.info('Client connected from {0}'.format(address))
			clientthread = ClientThread(clientsocket, address, self.matchmaking_q, self.reply_q)
			threading.Thread(target=clientthread.run).start()


class ServerCommand:

	FOUND, = range(1)

	def __init__(self, type):
		self.type = type

	def serialize(self):
		return '{{"cmd":{0}}}'.format(self.type)


class ClientCommand:

	QUEUE, ACCEPT, POSITION = range(3)

	def __init__(self, type, id, data, socket):
		self.type = type
		self.id = id
		self.data = data
		self.socket = socket


class ClientThread:

	def __init__(self, socket, address, matchmaking_q, reply_q):
		self.socket = socket
		self.address = address
		self.matchmaking_q = matchmaking_q
		self.reply_q = reply_q
		self.handlers = {
			ClientCommand.QUEUE: self._handle_queue,
			ClientCommand.ACCEPT: self._handle_accept
		}

	def run(self):
		while True:
			try:
				header = self._recv_n(4, False)
				msg_len = struct.unpack('<I', header)[0]
				data = self._recv_n(msg_len)
			except RuntimeError:
				pass
			else:
				try:
					data = json.loads(data)
				except ValueError:
					pass
				else:
					try:
						cmd = ClientCommand(data['cmd'], data['id'], data['data'], self.socket)
					except KeyError:
						pass
					else:
						self.handlers[cmd.type](cmd)
						while True:
							try:
								cmd = self.reply_q[self.socket]
							except KeyError:
								pass
							else:
								self._send(cmd.serialize())
								del self.reply_q[self.socket]
								break


	def _handle_queue(self, cmd): # Example: {\"cmd\":0,\"id\":1,\"data\":null}
		self.matchmaking_q.put_nowait(cmd)

	def _handle_accept(self, cmd): # Example: {\"cmd\":1,\"id\":1,\"data\":null}
		pass

	def _send(self, msg):
		msg = struct.pack('<I', len(msg)) + msg.encode('utf-8')
		totalsent = 0
		while totalsent < len(msg):
			sent = self.socket.send(msg[totalsent:])
			if sent == 0:
				raise RuntimeError("Error while sending.")
			totalsent += sent
		logging.info('Sent {0} bytes to {1}'.format(len(msg), self.address))

	def _recv_n(self, n, decode=True):
		data = b''
		while len(data) < n:
			chunk = self.socket.recv(n - len(data))
			if chunk == b'':
				raise RuntimeError("Error while receiving.")
			data += chunk
		logging.info('Received {0} bytes from {1}'.format(n, self.address))
		if decode:
			return data.decode('utf-8')
		return data
