import json
import logging
import queue
import socket
import struct
import threading

import server.matchmaker


class SocketServer:

	def __init__(self, host, port):
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.bind((host, port))
		self.server.listen(socket.SOMAXCONN)
		logging.info('Server listening on ' + str((host, port)))

		self.client_cmd_q = queue.Queue()
		self.server_cmd_q = {}

		matchmaker = server.matchmaker.Matchmaker(self.client_cmd_q, self.server_cmd_q)
		threading.Thread(target=matchmaker.run).start()

	def run(self):
		while True:
			(clientsocket, address) = self.server.accept()
			logging.info('Client connected from {0}'.format(address))
			clientthread = ClientThread(clientsocket, address, self.client_cmd_q, self.server_cmd_q)
			threading.Thread(target=clientthread.run).start()


class ServerCommand:

	FOUND = 'found'
	START = 'start'
	POSITION = 'position'
	WINNER = 'winner'
	LOSER = 'loser'

	def __init__(self, cmd, data=None):
		self.cmd = cmd
		self.data = data

	def serialize(self):
		return json.dumps(self.__dict__)


class ClientCommand:

	QUEUE = 'queue'
	CANCEL = 'cancel'
	ACCEPT = 'accept'
	DECLINE = 'decline'
	POSITION = 'position'

	def __init__(self, cmd, id, data, socket):
		self.cmd = cmd
		self.id = id
		self.data = data
		self.socket = socket


class ClientThread:

	def __init__(self, socket, address, client_cmd_q, server_cmd_q):
		self.socket = socket
		self.socket.settimeout(5.0)
		self.address = address
		self.client_cmd_q = client_cmd_q
		self.server_cmd_q = server_cmd_q
		self.server_cmd_q[self.socket] = queue.Queue()
		self.handlers = {
			ClientCommand.QUEUE: self._handle,
			ClientCommand.CANCEL: self._handle,
			ClientCommand.ACCEPT: self._handle,
			ClientCommand.DECLINE: self._handle,
			ClientCommand.POSITION: self._handle_position
		}

	def run(self):
		while True:
			try:
				header = self._recv_n(2, False)
				msg_len = struct.unpack('!h', header)[0]
				data = self._recv_n(msg_len)
			except IOError:
				pass # Error while receiving.
			else:
				try:
					data = json.loads(data)
					client_cmd = ClientCommand(data['cmd'], data['id'], data['data'], self.socket)
					self.handlers[client_cmd.cmd](client_cmd)
				except (ValueError, KeyError):
					pass # Ill-formed message (Invalid JSON/missing data/unknown command).
				else:
					logging.info('Received command {0} from {1}'.format(client_cmd.cmd.upper(), self.address))
				
			try:
				server_cmd = self.server_cmd_q[self.socket].get(timeout=1.0) # Might need to add a timeout here.
			except queue.Empty:
				pass
			else:
				self._send(server_cmd.serialize())
				logging.info('Sent command {0} to {1}'.format(server_cmd.cmd.upper(), self.address))

	def _handle(self, client_cmd):
		self.client_cmd_q.put(client_cmd)

	def _handle_position(self, client_cmd):
		pass

	def _send(self, msg):
		msg = struct.pack('!h', len(msg)) + msg.encode('utf-8')
		totalsent = 0
		while totalsent < len(msg):
			sent = self.socket.send(msg[totalsent:])
			if sent == 0:
				raise IOError
			totalsent += sent
		logging.info('Sent {0} bytes to {1}'.format(len(msg), self.address))

	def _recv_n(self, n, decode=True):
		data = b''
		while len(data) < n:
			chunk = self.socket.recv(n - len(data))
			if chunk == b'':
				raise IOError
			data += chunk
		logging.info('Received {0} bytes from {1}'.format(n, self.address))
		if decode:
			return data.decode('utf-8')
		return data
