from django.db import models


class Round(models.Model):
    round_id = models.UUIDField(primary_key=True)
    election_date = models.DateField(blank=True)
    number = models.IntegerField(default=1)


class Party:
    party_id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=200, blank=True)
    logo = models.CharField(max_length=200, blank=True)


class Candidate(models.Model):
    candidate_id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=200, blank=True)
    surname = models.CharField(max_length=200, blank=True)
    website = models.CharField(max_length=200, blank=True)

    party_id = models.ForeignKey(Party, on_delete=models.CASCADE)


class ElectionType(models.Model):
    type_id = models.IntegerField(default=0)
    type = models.CharField(max_length=200)
