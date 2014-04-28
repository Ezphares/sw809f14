import logging
import threading
from matchmaker import Matchmaker
from socketserver import SocketServer

def main():
	logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.DEBUG, datefmt='%m/%d/%Y %I:%M:%S')

	matchmaker = Matchmaker()
	threading.Thread(target=matchmaker.run).start()

	host = 'localhost'
	port = 9999
	server = SocketServer(host, port, matchmaker)
	threading.Thread(target=server.run).start()

if __name__ == "__main__":
	main()
