import random
import time


class Player:

	def __init__(self, rating, rd, distance):
		self.rating = rating
		self.rd = rd
		self.distance = distance
		self.search_width = 1
		self.last_increment = time.time()

	def max_rating_diff(self):
		return self.search_width * self.rd


class Matchmaker:

	def __init__(self):
		self.players = []
		self.distance_threshold = 0.15
		self.increment_time = 30.0
		self.increment = 0.25
		self.start_time = 0.0
		self.players_matched = 0
		self.total_rating_diff = 0
		self.total_dist_diff = 0
		self.total_wait_time = 0.0

	def run(self):
		index = 0
		self.start_time = time.time()
		while True:
			self._update_players()
			if len(self.players) >= 2 and time.time()-self.start_time < 120.0: # Stop when there are less than 2 players or 2 minutes has passed.
				player = self.players[index]
				best_match = self._get_best_match(player)
				if best_match is not None and self._get_best_match(best_match) is player:
					self._match(player, best_match)
				index = (index + 1) % len(self.players) if len(self.players) != 0 else 0
			else:
				return (self.players_matched,
						self.total_rating_diff/self.players_matched,
						self.total_dist_diff/self.players_matched,
						self.total_wait_time/self.players_matched)

	def enqueue(self, player):
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
		self.players_matched += 2
		self.total_rating_diff += self._rating_diff(player1, player2)
		self.total_dist_diff += abs(player1.distance-player2.distance)
		self.total_wait_time += 2*(time.time()-self.start_time)
		self.players.remove(player1)
		self.players.remove(player2)

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

	def _is_match(self, player1, player2):
		if self._distance_diff(player1, player2) <= self.distance_threshold:
			rating_diff = self._rating_diff(player1, player2)
			return rating_diff <= player1.max_rating_diff() and rating_diff <= player2.max_rating_diff()
		return False

	def _rating_diff(self, player1, player2):
		return abs(player1.rating-player2.rating)

	def _distance_diff(self, player1, player2):
		return abs(player1.distance-player2.distance)/min(player1.distance, player2.distance)


def main():
	runs = 10
	players = 100
	total_players_matched = 0
	total_rating_diff = 0
	total_dist_diff = 0
	total_wait_time = 0
	for i in range(runs):
		matchmaker = Matchmaker()
		for j in range(players):
			player = Player(random.randint(1000, 2000), random.randint(30, 350), random.randint(5000, 10000))
			matchmaker.enqueue(player)
		run = matchmaker.run()
		total_players_matched += run[0]
		total_rating_diff += run[1]
		total_dist_diff += run[2]
		total_wait_time += run[3]
		print(str(i+1) + ' & ' + str(run[0]) + ' & ' + str(round(run[1], 1)) + ' & ' + str(round(run[2], 1)) + ' & ' + str(round(run[3], 1)))
	print(str(round(total_players_matched/runs, 1)) + ' & ' + str(round(total_rating_diff/runs, 1)) + ' & ' + str(round(total_dist_diff/runs, 1)) + ' & ' + str(round(total_wait_time/runs, 1)))

if __name__ == "__main__": main()
