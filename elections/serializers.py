from rest_framework import serializers

from elections.models import Vote


class VoteSerializer(serializers.Serializer):
    model = Vote
    fields = (
        'vote_id',
        'candidate_id'
    )

    def save(self):
        pass
