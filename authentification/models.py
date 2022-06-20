import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models


class Voter(AbstractUser):
    voter_id = models.UUIDField(primary_key=True, default=uuid.uuid4())
    electoral_number = models.BigIntegerField(blank=True, default=0000)
    email = models.EmailField(max_length=300)
    username = models.CharField(max_length=200, blank=True, unique=True)

    permissions = models.ManyToManyField('elections.ElectionType')