import time

class Player:

	def __init__(self, id, rating, rd, socket):
		self.id = id
		self.rating = rating
		self.rd = rd
		self.socket = socket
		self.search_width = 1
		self.last_increment = int(time.time())

	def max_rating_diff(self):
		return self.search_width * self.rd
