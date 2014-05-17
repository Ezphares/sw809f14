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
		socket.setdefaulttimeout(5.0)
		logging.info('Server listening on ' + str((host, port)))

		self.client_cmd_q = queue.Queue()
		self.server_cmd_q = {}

		matchmaker = server.matchmaker.Matchmaker(self.client_cmd_q, self.server_cmd_q)
		threading.Thread(target=matchmaker.run).start()

	def run(self):
		while True:
			(clientsocket, address) = self.server.accept()
			clientsocket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
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
	POSITION = 'position'
	DISCONNECT = 'disconnect' # Only used internally.

	def __init__(self, cmd, socket, id=None, data=None):
		self.cmd = cmd
		self.socket = socket
		self.id = id
		self.data = data


class ClientThread:

	def __init__(self, socket, address, client_cmd_q, server_cmd_q):
		self.socket = socket
		self.address = address
		self.client_cmd_q = client_cmd_q
		self.server_cmd_q = server_cmd_q
		self.server_cmd_q[self.socket] = queue.Queue()
		self.handlers = {
			ClientCommand.QUEUE: self._handle,
			ClientCommand.CANCEL: self._handle,
			ClientCommand.ACCEPT: self._handle,
			ClientCommand.POSITION: self._handle_position
		}

	def run(self):
		while True:
			header = self._recv_n(2, False) # Get message length as 2 bytes.
			if header is False: # Clean disconnect from client detected.
				self._close()
				break;
			elif header is not None:
				msg_len = struct.unpack('!h', header)[0] # Convert message length to 16 bit integer.
				data = self._recv_n(msg_len)
				if data == False: # Clean disconnect from client detected.
					self._close()
					break
				try:
					data = json.loads(data)
					client_cmd = ClientCommand(data['cmd'], self.socket, data['id'], data['data'])
					self.handlers[client_cmd.cmd](client_cmd)
				except (ValueError, KeyError): # Ill-formed message (Invalid JSON/missing data/unknown command).
					pass
				else:
					logging.info('Received command {0} from {1}'.format(client_cmd.cmd.upper(), self.address))

			try:
				server_cmd = self.server_cmd_q[self.socket].get_nowait()
			except queue.Empty:
				pass
			else:
				if self._send(server_cmd.serialize()) == None: # Message not sent.
					self.server_cmd_q[self.socket].put(server.cmd) # Put the message back in the queue.
				else:
					logging.info('Sent command {0} to {1}'.format(server_cmd.cmd.upper(), self.address))

	def _handle(self, client_cmd):
		self.client_cmd_q.put(client_cmd)

	def _handle_position(self, client_cmd):
		pass

	def _send(self, msg):
		msg = struct.pack('!h', len(msg)) + msg.encode('utf-8')
		totalsent = 0
		while totalsent < len(msg):
			try:
				sent = self.socket.send(msg[totalsent:])
			except socket.timeout:
				return None
			else:
				totalsent += sent
		logging.info('Sent {0} bytes to {1}'.format(len(msg), self.address))
		return True

	def _recv_n(self, n, decode=True):
		data = b''
		while len(data) < n:
			try:
				chunk = self.socket.recv(n - len(data))
			except socket.timeout:
				return None
			else:
				if chunk == b'':
					return False
				data += chunk
		logging.info('Received {0} bytes from {1}'.format(n, self.address))
		if decode:
			return data.decode('utf-8')
		return data

	def _close(self):
		self.socket.shutdown(socket.SHUT_RDWR)
		self.socket.close()

		# Tell the matchmaker to perform cleanup operations, if any.
		client_cmd = ClientCommand(cmd=ClientCommand.DISCONNECT, socket=self.socket)
		self.client_cmd_q.put(client_cmd)

		logging.info('Client {0} disconnected'.format(self.address))
