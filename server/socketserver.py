import json
import logging
import queue
import select
import socket
from matchmaker import Matchmaker
from player import Player

class SocketServer:

	def __init__(self, host, port, matchmaker):
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.setblocking(0)
		self.server.bind((host, port))
		self.server.listen(socket.SOMAXCONN)
		logging.info('Server listening on port ' + str(port))

		self.matchmaker = matchmaker
		self.readers = [self.server]
		self.writers = []
		self.msg_queues = {}

	def run(self):
		while True:
			(readable, writable, in_error) = select.select(self.readers,
														   self.writers,
														   self.readers)
			self._handle_inputs(readable)
			self._handle_outputs(writable)
			self._handle_errors(in_error)

	def send_msg(self, s, msg):
		self.msg_queues[s].put(msg)

	def _handle_inputs(self, readable):
		for s in readable:
			if s is self.server: # Server socket is readble => client is connecting.
				(client, address) = self.server.accept()
				client.setblocking(0)
				logging.info('New connection from ' + str(client.getpeername()))
				self.readers.append(client)
				self.msg_queues[client] = queue.Queue()
			else: # Client socket is readable.
				data = s.recv(1024)
				if data:
					logging.info(str(len(data)) + ' bytes received from ' + str(s.getpeername()))
					self._parse_msg(data)
					if s not in self.writers:
						self.writers.append(s)
				else: # Client socket is readble but no data => client has disconnected.
					self._close_socket(s)

	def _handle_outputs(self, writable):
		for s in writable:
			if s in self.msg_queues:
				try:
					msg = self.msg_queues[s].get_nowait()
				except queue.Empty:
					self.writers.remove(s)
				else:
					s.send(msg)

	def _handle_errors(self, in_error):
		for s in in_error:
			self._close_socket(s)

	def _close_socket(self, s):
		logging.info(str(s.getpeername()) + ' disconnected')
		s.close()
		if s in self.writers:
			self.writers.remove(s)
		if s in self.readers:
			self.readers.remove(s)
		del self.msg_queues[s]

	def _parse_msg(self, data):
		msg = json.loads(data.decode('utf-8'))
		try:
			cmd = msg['cmd']
		except KeyError:
			return # Error

		if cmd == 'queue':
			pass
		elif cmd == 'accept':
			pass
		elif cmd == 'position':
			pass
		else:
			pass # Error
