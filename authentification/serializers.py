from rest_framework import serializers

from authentification.models import Voter


class VoterSerializer(serializers.ModelSerializer):
    model = Voter
    fields = (
        'voter_id',
        'email',
        'name',
        'surname'
    )