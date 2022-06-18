from rest_framework import serializers

from authentification.models import Voter


class VoterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voter
        fields = (
            'voter_id',
            'email',
            'name',
            'surname',
            'password',
            'username'
        )

    def save(self, **kwargs):
        voter = Voter(
            email=self.validated_data['email'],
            name=self.validated_data['name'],
            surname=self.validated_data['surname'],
            last_name=self.validated_data['name'],
            first_name=self.validated_data['surname'],
            voter_id=self.validated_data['voter_id'],
            username=self.validated_data['username']
        )

        voter.set_password(self.validated_data['password'])
        voter.save()

        return voter
