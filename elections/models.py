from django.db import models

from authentification.models import Voter


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
    type_id = models.IntegerField(primary_key=True, default=0)
    type = models.CharField(max_length=200)


class Election(models.Model):
    election_id = models.UUIDField(primary_key=True, default=0)
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)


class Participate(models.Model):
    election_id = models.ForeignKey(Election, on_delete=models.CASCADE)
    candidate_id = models.ForeignKey(Candidate, on_delete=models.CASCADE)


class ElectionProgress(models.Model):
    election_id = models.ForeignKey(Election, on_delete=models.CASCADE)
    round_id = models.ForeignKey(Round, on_delete=models.CASCADE)


class Vote(models.Model):
    vote_id = models.UUIDField(primary_key=True)
    candidate_id = models.ForeignKey(Candidate, on_delete=models.CASCADE)


class Submit(models.Model):
    round_id = models.ForeignKey(Round, on_delete=models.CASCADE)
    vote_id = models.ForeignKey(Vote, on_delete=models.CASCADE)


class Logs(models.Model):
    voter_id = models.ForeignKey(Voter, on_delete=models.CASCADE)
    round_id = models.ForeignKey(Round, on_delete=models.CASCADE)


class Permissions(models.Model):
    voter_id = models.ForeignKey(Voter, on_delete=models.CASCADE)
    type_id = models.ForeignKey(ElectionType, on_delete=models.CASCADE)