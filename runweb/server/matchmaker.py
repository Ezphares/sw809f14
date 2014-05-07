import logging
import queue
import time

import competitive.models

import server.socketserver


class Player:

	def __init__(self, model, socket):
		self.model = model
		self.socket = socket
		self.search_width = 1
		self.last_increment = int(time.time())

	def __str__(self):
		return '(id: {0}, rating: {1}, rd: {2})'.format(self.id, self.rating, self.rd)

	@property
	def id(self):
		return self.model.user.pk

	@property
	def rating(self):
		return self.model.rating

	@property
	def rd(self):
		return self.model.rd

	def max_rating_diff(self):
		return self.search_width * self.rd


class Match:

	def __init__(self, player1, player2):
		self.player1 = player1
		self.player2 = player2
		self.player1_accept = False
		self.player2_accept = False


class Matchmaker:

	def __init__(self, client_cmd_q, server_cmd_q):
		self.client_cmd_q = client_cmd_q
		self.server_cmd_q = server_cmd_q
		self.players = []
		self.matches = []
		self.increment_time = 30
		self.increment = 0.1
		self.handlers = {
			server.socketserver.ClientCommand.QUEUE: self._handle_queue,
			server.socketserver.ClientCommand.CANCEL: self._handle_cancel,
			server.socketserver.ClientCommand.ACCEPT: self._handle_accept,
			server.socketserver.ClientCommand.DECLINE: self._handle_decline
		}
		logging.info('Matchmaker started')

	def run(self):
		index = 0
		while True: # TODO: This is super inefficient. Need to introduce some kind of blocking.
			while True:
				try:
					client_cmd = self.client_cmd_q.get_nowait()
				except queue.Empty:
					break
				self.handlers[client_cmd.cmd](client_cmd)

			if len(self.players) >= 2: # Need at least two players.
				self._update_players()
				player = self.players[index]
				best_match = self._get_best_match(player)
				if best_match and self._get_best_match(best_match) is player:
					self._match(player, best_match)
				index = (index + 1) % len(self.players) if len(self.players) != 0 else 0

	# TODO: Make sure that a player can only queue once.
	def _handle_queue(self, client_cmd):
		player = Player(competitive.models.Player.objects.get(pk=client_cmd.id), client_cmd.socket)
		self._enqueue_player(player)

	def _handle_cancel(self, client_cmd):
		self._dequeue_player(client_cmd.id)

	def _handle_accept(self, client_cmd):
		for match in self.matches:
			if match.player1.id == client_cmd.id:
				match.player1_accept = True
			elif match.player2.id == client_cmd.id:
				match.player2_accept = True
			else: # Neither player1 nor player2.
				continue

			if match.player1_accept and match.player2_accept:
				competitive.models.Match(player1=match.player1.model, player2=match.player2.model).save()
				server_cmd = server.socketserver.ServerCommand(server.socketserver.ServerCommand.START)
				self.server_cmd_q[match.player1.socket].put(server_cmd)
				self.server_cmd_q[match.player2.socket].put(server_cmd)
				self.matches.remove(match)
			break

	def _handle_decline(self, client_cmd):
		for match in self.matches:
			if match.player1.id == client_cmd.id:
				self._dequeue_player(match.player1.id)
				self._enqueue_player(match.player2)
			elif match.player2.id == client_cmd.id:
				self._dequeue_player(match.player2.id)
				self._enqueue_player(match.player1)
			else:
				continue
			self.matches.remove(match)
			break

	def _enqueue_player(self, player):
		logging.info('Player queued {0}'.format(str(player)))
		high = len(self.players)
		low = 0
		while low < high:
			mid = (low+high)//2
			if self.players[mid].rating > player.rating:
				high = mid
			else:
				low = mid+1
		self.players.insert(low, player)
		logging.info('Players in queue {0}'.format(str(len(self.players))))

	def _dequeue_player(self, id):
		for player in self.players:
			if player.id == id:
				self.players.remove(player)
				break

	def _update_players(self):
		now = int(time.time())
		for player in self.players:
			if now - player.last_increment >= self.increment_time:
				player.search_width += self.increment
				player.last_increment = now

	def _match(self, player1, player2):
		logging.info('Matched player {0} against player {1}'.format(str(player1), str(player2)))
		match = Match(player1, player2)
		self.matches.append(match)
		server_cmd = server.socketserver.ServerCommand(server.socketserver.ServerCommand.FOUND)
		self.server_cmd_q[player1.socket].put(server_cmd)
		self.server_cmd_q[player2.socket].put(server_cmd)
		self.players.remove(player1)
		self.players.remove(player2)
		logging.info('Players in queue {0}'.format(str(len(self.players))))

	def _rating_diff(self, player1, player2):
		return abs(player1.rating-player2.rating)

	def _is_match(self, player1, player2):
		rating_diff = self._rating_diff(player1, player2)
		return rating_diff <= player1.max_rating_diff() and rating_diff <= player2.max_rating_diff()

	def _get_best_match(self, player):
		index = self.players.index(player)
		if index == 0: # Lowest rated player. Only check RHS.
			best_match = self.players[index+1]
		elif index == len(self.players)-1: # Highest rated player. Only check LHS.
			best_match = self.players[index-1]
		else: # Neither lowest nor highest rated player. Check both LHS and RHS.
			opponent_left = self.players[index-1]
			opponent_right = self.players[index+1]
			if self._rating_diff(player, opponent_left) < self._rating_diff(player, opponent_right):
				best_match = opponent_left
			else:
				best_match = opponent_right

		if self._is_match(player, best_match):
			return best_match
