import logging
import threading
from django.core.management.base import BaseCommand, CommandError
from server.socketserver import SocketServer
from server.matchmaker import Matchmaker

class Command(BaseCommand):
	help = 'Starts the matchmaking server. Usage: manage.py startserver <host> <port>'

	def handle(self, *args, **options):
		try:
			host = args[0]
		except IndexError:
			raise CommandError('No host supplied.')

		try:
			port = args[1]
		except IndexError:
			raise CommandError('No port supplied')
		else:
			try:
				port = int(port)
			except ValueError:
				raise CommandError('Port must be an integer.')

		logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.DEBUG, datefmt='%m/%d/%Y %I:%M:%S')

		matchmaker = Matchmaker()
		threading.Thread(target=matchmaker.run).start()

		server = SocketServer(host, port, matchmaker)
		threading.Thread(target=server.run).start()
