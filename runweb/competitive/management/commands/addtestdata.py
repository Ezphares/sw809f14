from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

import competitive.models


class Command(BaseCommand):
	help = 'Populates the database with test data. Usage: manage.py addtestdata'

	def handle(self, *args, **options):
		competitive.models.Player(user=User.objects.create_user('test1', 'test@test.com', 'test'), rating=1500, rd=100).save()
		competitive.models.Player(user=User.objects.create_user('test2', 'test@test.com', 'test'), rating=1575, rd=50).save()
		competitive.models.Player(user=User.objects.create_user('test3', 'test@test.com', 'test'), rating=1550, rd=50).save()
		competitive.models.Player(user=User.objects.create_user('test4', 'test@test.com', 'test'), rating=1605, rd=100).save()