from django.db import models


class Party(models.Model):
    party_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True)
    website = models.CharField(max_length=100, blank=True)
    logo = models.CharField(max_length=700, blank=True)

    def __str__(self):
        return {
            "party_id": self.party_id,
            "name": self.name,
            "website": self.website,
            "logo": self.logo
        }.__str__()


class ElectionType(models.Model):
    type_id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.type}'.__str__()


class Round(models.Model):
    round_id = models.IntegerField(primary_key=True)
    date = models.DateField(blank=True)

    def __str__(self):
        return {"round_id": self.round_id, "date": self.date}.__str__()


class Election(models.Model):
    election_id = models.IntegerField(primary_key=True)
    type = models.ForeignKey(ElectionType, on_delete=models.CASCADE)

    progress = models.ManyToManyField(Round)

    def __str__(self):
        return {
            "election_id": self.election_id,
            "type": self.type.__str__()
        }.__str__()


class Candidate(models.Model):
    candidate_id = models.IntegerField(primary_key=True)
    last_name = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(max_length=100, blank=True)

    party = models.ForeignKey(Party, on_delete=models.CASCADE)
    elections = models.ManyToManyField(Election)

    def __str__(self):
        return {
            "candidate_id": self.candidate_id,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "party_id": self.party,
        }.__str__()


class Vote(models.Model):
    vote_id = models.UUIDField(primary_key=True)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    submissions = models.ManyToManyField(Round)

    def __str__(self):
        return {
            "vote_id": self.vote_id,
            "candidate": self.candidate.__str__()
        }.__str__()


