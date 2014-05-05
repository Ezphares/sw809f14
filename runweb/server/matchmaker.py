import logging
import time

from competitive.models import Profile

import server.socketserver

class Player:

	def __init__(self, profile, socket):
		self.profile = profile
		self.socket = socket
		self.search_width = 1
		self.last_increment = int(time.time())

	def __str__(self):
		return '(id: {0}, rating: {1}, rd: {2})'.format(self.profile.user.id, self.profile.rating, self.profile.rd)

	@property
	def id(self):
		return self.profile.id

	@property
	def rating(self):
		return self.profile.rating

	@property
	def rd(self):
		return self.profile.rd

	def max_rating_diff(self):
		return self.search_width * self.profile.rd


class Matchmaker:

	def __init__(self, matchmaking_q, reply_q):
		self.matchmaking_q = matchmaking_q
		self.reply_q = reply_q
		self.players = []
		self.increment_time = 30
		self.increment = 0.1
		logging.info('Matchmaker started')

	def run(self):
		index = 0
		while True:
			while not self.matchmaking_q.empty():
				cmd = self.matchmaking_q.get_nowait()
				player = Player(Profile.objects.get(pk=cmd.id), cmd.socket)
				self._add_player(player)

			if len(self.players) >= 2: # Need at least two players.
				self._update_players()
				player = self.players[index]
				best_match = self._get_best_match(player)
				if best_match and self._get_best_match(best_match) is player:
					self._match(player, best_match)
				index = (index + 1) % len(self.players) if len(self.players) != 0 else 0
			else:
				pass
				# Yield thread.

	def _add_player(self, player):
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

	def _update_players(self):
		now = int(time.time())
		for player in self.players:
			if now - player.last_increment >= self.increment_time:
				player.search_width += self.increment
				player.last_increment = now

	def _match(self, player1, player2):
		logging.info('Matched player {0} against player {1}'.format(str(player1), str(player2)))
		cmd = server.socketserver.ServerCommand(server.socketserver.ServerCommand.FOUND)
		self.reply_q[player1.socket] = cmd
		self.reply_q[player2.socket] = cmd
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
