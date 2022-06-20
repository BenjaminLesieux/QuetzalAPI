from django.db import models


class Party(models.Model):
    party_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True)
    website = models.CharField(max_length=100, blank=True)
    logo = models.CharField(max_length=700, blank=True)


class ElectionType(models.Model):
    type_id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.type} ({self.type_id})'


class Round(models.Model):
    round_id = models.IntegerField(primary_key=True)
    date = models.DateField(blank=True)

    def __str__(self):
        return {"round_id": self.round_id, "date": self.date}


class Election(models.Model):
    election_id = models.IntegerField(primary_key=True)
    type = models.ForeignKey(ElectionType, on_delete=models.CASCADE)

    progress = models.ManyToManyField(Round)

    def __str__(self):
        return str(self.election_id)


class Candidate(models.Model):
    candidate_id = models.IntegerField(primary_key=True)
    last_name = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(max_length=100, blank=True)

    party = models.ForeignKey(Party, on_delete=models.CASCADE)
    elections = models.ManyToManyField(Election)


class Vote(models.Model):
    vote_id = models.UUIDField(primary_key=True)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    submissions = models.ManyToManyField(Round)


