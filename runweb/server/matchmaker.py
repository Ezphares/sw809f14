import logging
import time
from server.player import Player

class Matchmaker:

	def __init__(self):
		self.players = []
		self.increment_time = 30
		self.increment = 0.1

	def run(self):
		index = 0
		while True:
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

	def add_player(self, player):
		high = len(self.players)
		low = 0
		while low < high:
			mid = (low+high)//2
			if self.players[mid].rating > player.rating:
				high = mid
			else:
				low = mid+1
		self.players.insert(low, player)

	def _update_players(self):
		now = int(time.time())

		for player in self.players:
			if now - player.last_increment >= self.increment_time:
				player.search_width += self.increment
				player.last_increment = now

	def _match(self, player1, player2):
		logging.info('Matched player ' + str(player1.id) + ' with player ' + str(player2.id))
		self.players.remove(player1)
		self.players.remove(player2)

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
