from django.contrib.auth.models import AbstractUser
from django.db import models


class UserInfo(models.Model):
    voter_id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    surname = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'UserInfo'

