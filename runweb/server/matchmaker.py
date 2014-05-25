import logging
import queue
import time

import competitive.models
import routes.models
import server.socketserver


class Player:

	def __init__(self, model, route, socket):
		self.model = model
		self.route = route
		self.socket = socket
		self.position = 0
		self.completion = 0
		self.search_width = 1
		self.last_increment = int(time.time())

	def __str__(self):
		return '(id: {0}, rating: {1}, rd: {2}, distance: {3})'.format(self.id, self.rating, self.rd, self.distance)

	@property
	def id(self):
		return self.model.user.pk

	@property
	def rating(self):
		return self.model.rating

	@rating.setter
	def rating(self, value):
		self.model.rating = value

	@property
	def rd(self):
		return self.model.rd

	@rd.setter
	def rd(self, value):
		self.model.rd = value

	@property
	def last_match(self):
		return self.model.last_match

	@last_match.setter
	def last_match(self, value):
		self.model.last_match = value

	@property
	def distance(self):
		return self.route.distance

	def max_rating_diff(self):
		return self.search_width * self.rd


class Match:

	def __init__(self, player1, player2):
		self.player1 = player1
		self.player2 = player2
		self.player1_accept = False
		self.player2_accept = False
		self.found_time = int(time.time())

	def __str__(self):
		return '({0} vs. {1})'.format(self.player1, self.player2)


class Matchmaker:

	def __init__(self, client_cmd_q, server_cmd_q, matches):
		self.distance_threshold = 0.15
		self.increment_time = 30
		self.increment = 0.25
		self.accept_time = 20
		self.client_cmd_q = client_cmd_q
		self.server_cmd_q = server_cmd_q
		self.matches = matches
		self.temp_matches = []
		self.players = []
		self.handlers = {
			server.socketserver.ClientCommand.QUEUE: self._handle_queue,
			server.socketserver.ClientCommand.CANCEL: self._handle_cancel,
			server.socketserver.ClientCommand.ACCEPT: self._handle_accept,
			server.socketserver.ClientCommand.DISCONNECT: self._handle_disconnect
		}
		logging.info('Matchmaker started')

	def run(self):
		index = 0
		while True:
			while True:
				try:
					client_cmd = self.client_cmd_q.get_nowait()
				except queue.Empty:
					break
				self.handlers[client_cmd.cmd](client_cmd)
			self._check_matches()
			self._update_players()
			if len(self.players) >= 2: # Need at least two players.
				player = self.players[index]
				best_match = self._get_best_match(player)
				if best_match is not None and self._get_best_match(best_match) is player:
					self._match(player, best_match)
				index = (index + 1) % len(self.players) if len(self.players) != 0 else 0
			time.sleep(0.01)

	def _handle_queue(self, client_cmd):
			player = Player(competitive.models.Player.objects.get(pk=client_cmd.id),
							routes.models.Route.objects.get(pk=client_cmd.data['route_id']),
							client_cmd.socket)
			self._enqueue(player)

	def _handle_cancel(self, client_cmd):
		self._dequeue(client_cmd.id)

	def _handle_accept(self, client_cmd):
		for i, match in enumerate(self.temp_matches):
			if match.player1.id == client_cmd.id:
				match.player1_accept = True
			elif match.player2.id == client_cmd.id:
				match.player2_accept = True
			else: # Neither player1 nor player2.
				continue

			if match.player1_accept and match.player2_accept:
				server_cmd = server.socketserver.ServerCommand(server.socketserver.ServerCommand.START)
				self.server_cmd_q[match.player1.socket].put(server_cmd)
				self.server_cmd_q[match.player2.socket].put(server_cmd)
				self.matches.append(self.temp_matches.pop(i))
			break

	def _handle_disconnect(self, client_cmd):
		for player in self.players:
			if player.socket is client_cmd.socket:
				self._dequeue(player.id)
				break

	def _enqueue(self, player):
		if self._get_player(player.id) is None: # Ensure that the player is not already queued.
			self.players.append(player)
			logging.info('Player queued {0}'.format(str(player)))
			logging.info('Players in queue {0}'.format(str(len(self.players))))

	def _dequeue(self, id):
		player = self._get_player(id)
		if player is not None: # Ensure that the player is queued.
			self.players.remove(player)
			logging.info('Player dequeued {0}'.format(str(player)))
			logging.info('Players in queue {0}'.format(str(len(self.players))))

	def _match(self, player1, player2):
		match = Match(player1, player2)
		self.temp_matches.append(match)
		server_cmd = server.socketserver.ServerCommand(server.socketserver.ServerCommand.FOUND)
		self.server_cmd_q[player1.socket].put(server_cmd)
		self.server_cmd_q[player2.socket].put(server_cmd)
		logging.info('Match found {0}'.format(str(match)))
		self._dequeue(player1.id)
		self._dequeue(player2.id)

	def _check_matches(self):
		now = int(time.time())
		for match in self.temp_matches:
			if now - match.found_time >= self.accept_time:
				self.temp_matches.remove(match)
				logging.info('Match not accepted in time {0}'.format(str(match)))

	def _update_players(self):
		now = int(time.time())
		for player in self.players:
			if now - player.last_increment >= self.increment_time:
				player.search_width += self.increment
				player.last_increment = now

	def _get_player(self, id):
		for player in self.players:
			if player.id == id:
				return player

	def _rating_diff(self, player1, player2):
		return abs(player1.rating-player2.rating)

	def _distance_diff(self, player1, player2):
		return abs(player1.distance-player2.distance)/min(player1.distance, player2.distance)

	def _is_match(self, player1, player2):
		if self._distance_diff(player1, player2) <= self.distance_threshold:
			rating_diff = self._rating_diff(player1, player2)
			return rating_diff <= player1.max_rating_diff() and rating_diff <= player2.max_rating_diff()
		return False

	def _get_best_match(self, player):
		best_match = None
		for opponent in self.players:
			if opponent is player:
				continue
			if self._is_match(player, opponent):
				if best_match is not None:
					if self._rating_diff(player, opponent) < self._rating_diff(player, best_match):
						best_match = opponent
				else:
					best_match = opponent
		return best_match
