from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


class Voter(AbstractBaseUser):
    voter_id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=200, blank=True)
    surname = models.CharField(max_length=200, blank=True)
