import uuid

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class Voter(AbstractUser):
    voter_id = models.UUIDField(primary_key=True, default=uuid.uuid4())
    electoral_number = models.BigIntegerField(blank=False, unique=True)

    permissions = models.ManyToManyField('elections.ElectionType')
    votes = models.ManyToManyField('elections.Round')

    username = models.CharField(max_length=100, default="None")

    USERNAME_FIELD = 'electoral_number'
    REQUIRED_FIELDS = ('email', 'last_name', 'first_name', 'username')

    def __str__(self):
        return self.last_name + " " + self.first_name


class ElectoralNumbers(models.Model):
    """
    This class just contains all the allowed electoral numbers. When creating a new Voter
    its electoral_number must be stored in this table with the right last_name and first_name
    """

    electoral_number = models.BigIntegerField(blank=False, unique=True)

    last_name = models.CharField(max_length=200, blank=True)
    first_name = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f'{self.last_name} {self.first_name} : {self.electoral_number}'

