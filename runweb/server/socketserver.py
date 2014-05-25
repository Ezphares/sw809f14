import datetime
import json
import logging
import queue
import socket
import struct
import threading

import competitive.models
import server.glicko
import server.matchmaker


class SocketServer:

	def __init__(self, host, port):
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.bind((host, port))
		self.server.listen(socket.SOMAXCONN)
		socket.setdefaulttimeout(1.0)
		logging.info('Server listening on ' + str((host, port)))

		self.client_cmd_q = queue.Queue()
		self.server_cmd_q = {} # One entry for each client thread containing a Queue.
		self.matches = []

		matchmaker = server.matchmaker.Matchmaker(self.client_cmd_q, self.server_cmd_q, self.matches)
		threading.Thread(target=matchmaker.run).start()

	def run(self):
		while True:
			(clientsocket, address) = self.server.accept()
			clientsocket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
			logging.info('Client connected from {0}'.format(address))
			clientthread = ClientThread(clientsocket, address, self.client_cmd_q, self.server_cmd_q, self.matches)
			threading.Thread(target=clientthread.run).start()


class ServerCommand:

	FOUND = 'found'
	START = 'start'
	POSITION = 'position'
	WINNER = 'winner'

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

	def __init__(self, socket, address, client_cmd_q, server_cmd_q, matches):
		self.socket = socket
		self.address = address
		self.client_cmd_q = client_cmd_q
		self.server_cmd_q = server_cmd_q
		self.matches = matches
		self.glicko = server.glicko.Glicko(18.1)
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
			if header is False: # Client disconnected.
				break
			elif header is not None:
				msg_len = struct.unpack('!h', header)[0] # Convert message length to 16 bit integer.
				data = self._recv_n(msg_len)
				if data == False: # Client disconnected.
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
				server_cmd = self.server_cmd_q[self.socket].get_nowait() # Try to a get a command.
			except queue.Empty: # No commands available.
				pass
			else: # If there was a command, try to send it.
				status = self._send(server_cmd.serialize())
				if status is None: # Timed out. Put the command back in the queue.
					self.server_cmd_q[self.socket].put(server_cmd)
				elif status is False: # Client disconnected.
					break
				else:
					logging.info('Sent command {0} to {1}'.format(server_cmd.cmd.upper(), self.address))
		self._close()

	def _handle(self, client_cmd):
		self.client_cmd_q.put(client_cmd)

	def _handle_position(self, client_cmd):
		for match in self.matches:
			if match.player1.id == client_cmd.id:
				player = match.player1
				opponent = match.player2
			elif match.player2.id == client_cmd.id:
				player = match.player2
				opponent = match.player1
			else:
				continue
			currentmatch = match
			break
		else: # Match not found.
			return
		polyline = player.route.get_polyline()
		(current, total, completed) = polyline.advance(player.position,
													   (client_cmd.data['lng'], client_cmd.data['lat']))
		if completed:
			self._finish_match(player, opponent, currentmatch)
		else:
			if polyline.on_route((client_cmd.data['lng'], client_cmd.data['lat'])):
				player.position = current
				player.completion = current/total
				server_cmd = ServerCommand(ServerCommand.POSITION, {'completion': opponent.completion})
				self.server_cmd_q[player.socket].put(server_cmd)
			else:
				self._finish_match(opponent, player, currentmatch)


	def _finish_match(self, winner, loser, match):
		self.matches.remove(match)
		server_cmd = ServerCommand(ServerCommand.WINNER, {'result': winner.id})
		self.server_cmd_q[winner.socket].put(server_cmd)
		self.server_cmd_q[loser.socket].put(server_cmd)
		self._update_rating(winner, loser, 1)
		self._update_rating(loser, winner, 0)
		competitive.models.Match(winner=winner.id, loser=loser.id).save()

	def _update_rating(self, player, opponent, outcome):
		last_match = player.last_match
		today = datetime.date.today()
		days_since_last_match = (today-last_match).days if last_match is not None else 0
		(rating, rd) = self.glicko.update_player(player.rating,
												 player.rd,
												 opponent.rating,
												 opponent.rd,
												 days_since_last_match,
												 outcome)
		player.rating = rating
		player.rd = rd
		player.last_match = today
		player.model.save()

	def _send(self, msg):
		msg = struct.pack('!h', len(msg)) + msg.encode('utf-8')
		totalsent = 0
		while totalsent < len(msg):
			try:
				sent = self.socket.send(msg[totalsent:])
			except socket.timeout:
				return None
			except:
				return False
			else:
				if sent == 0:
					return False
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
			except:
				return False
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
