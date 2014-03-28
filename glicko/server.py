import socket
import threading
import logging
import json
import time

class SocketServer:

	def __init__(self, host, port, on_connect):
		self.host = host
		self.port = port
		self.on_connect = on_connect

	def start(self):
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_socket.bind((self.host, self.port))
		server_socket.listen(socket.SOMAXCONN)

		while True:
			(connection, address) = server_socket.accept()
			self.on_connect(connection)
			logging.info('Client connected: ' + address[0] + ':' + str(address[1]));

class MatchMaker:

	def __init__(self):
		self.players = []
		self.increment_time = 30
		self.increment = 0.1

	def _update_players(self):
		now = int(time.time())

		for player in self.players:
			if now - player.last_increment >= self.increment_time:
				player.search_width += self.increment
				player.last_increment = now

	def _overlap(self, player1, player2):
		return max(0, min(player1.max_rating(), player2.max_rating()) - max(player1.min_rating(), player2.min_rating()))

	def add_player(self, connection):
		data = json.loads(connection.recv(1024).decode('utf-8'))
		player = Player(data['id'], data['rating'], data['rd'], connection)
		self.players.append(player)
		logging.info('Player added: ' + str(data))

	def start(self):
		while True:
			self._update_players()
			for player in self.players:
				best_match = None
				for opponent in self.players:
					if player == opponent:
						continue
					if self._overlap(player, opponent) > 0:
						if best_match == None or abs(player.rating - opponent.rating) < abs(player.rating - best_match.rating):
							best_match = opponent
				if best_match is not None:
					logging.info('Match found: ' + str(player.id) + ' vs. ' + str(opponent.id))
					self.players.remove(player)
					self.players.remove(opponent)
					# Start the match!

class Player:

	def __init__(self, id, rating, rd, connection):
		self.id = id
		self.rating = rating
		self.rd = rd
		self.connection = connection
		self.search_width = 1
		self.last_increment = int(time.time())

	def __eq__(self, other):
		return self.id == other.id

	def min_rating(self):
		return self.rating - self.rd * self.search_width

	def max_rating(self):
		return self.rating + self.rd * self.search_width

def main():
	logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.DEBUG, datefmt='%m/%d/%Y %I:%M:%S')

	matchmaker = MatchMaker()
	matchmaker_thread = threading.Thread(target=matchmaker.start)
	matchmaker_thread.start()

	host = 'localhost'
	port = 9999
	server = SocketServer(host, port, matchmaker.add_player)
	server_thread = threading.Thread(target=server.start)
	server_thread.start()

if __name__ == "__main__":
	main()
