from django.db import models
from django.contrib.auth.models import User

class Friend(models.Model):
    from_user = models.ForeignKey(User)
    to_user = models.ForeignKey(User, related_name = 'received_requests')
    accepted = models.BooleanField(default = False)

