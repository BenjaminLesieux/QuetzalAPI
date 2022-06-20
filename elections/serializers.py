from rest_framework import serializers

from elections.models import Vote, Election


class VoteSerializer(serializers.Serializer):
    model = Vote
    fields = (
        'vote_id',
        'candidate_id'
    )

    def save(self):
        pass


class ElectionSerializer(serializers.Serializer):
    model = Election
    fields = (
        'election_id',
        'type'
    )
