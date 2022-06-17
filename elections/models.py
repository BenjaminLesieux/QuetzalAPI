from django.db import models


class Party(models.Model):
    party_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    logo = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'elections_party'


class Candidate(models.Model):
    candidate_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    surname = models.CharField(max_length=100, blank=True, null=True)
    website = models.CharField(max_length=100, blank=True, null=True)
    party_id = models.ForeignKey('Party', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'elections_candidate'


class Election(models.Model):
    election_id = models.BigIntegerField(primary_key=True)
    start_end = models.DateField(blank=True, null=True)
    end_date = models.CharField(max_length=50, blank=True, null=True)
    type = models.ForeignKey('elections.ElectionType', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'elections_election'


class ElectionProgress(models.Model):
    election = models.OneToOneField(Election, models.DO_NOTHING, primary_key=True)
    round = models.ForeignKey('Round', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'elections_electionprogress'
        unique_together = (('election', 'round'),)


class ElectionType(models.Model):
    type_id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'elections_electiontype'


class Logs(models.Model):
    voter = models.OneToOneField('authentification.Voter', models.DO_NOTHING, primary_key=True)
    round = models.ForeignKey('Round', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'elections_logs'
        unique_together = (('voter', 'round'),)


class Participate(models.Model):
    election = models.OneToOneField(Election, models.DO_NOTHING, primary_key=True)
    candidate = models.ForeignKey(Candidate, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'elections_participate'
        unique_together = (('election', 'candidate'),)


class Permissions(models.Model):
    voter = models.OneToOneField('authentification.Voter', models.DO_NOTHING, primary_key=True)
    type = models.ForeignKey(ElectionType, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'elections_permissions'
        unique_together = (('voter', 'type'),)


class Round(models.Model):
    round_id = models.BigIntegerField(primary_key=True)
    election_date = models.DateField(blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'elections_round'


class Vote(models.Model):
    vote_id = models.BigIntegerField(primary_key=True)
    candidate = models.ForeignKey(Candidate, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'elections_vote'


class Submit(models.Model):
    round = models.OneToOneField(Round, models.DO_NOTHING, primary_key=True)
    vote = models.ForeignKey(Vote, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'elections_submit'
        unique_together = (('round', 'vote'),)

