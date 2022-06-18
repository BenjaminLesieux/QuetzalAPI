import re
from authentification.validators import is_valid
from django.contrib.auth import password_validation
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from authentification.models import Voter
import regex


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

        password = (self.validated_data['password'])

        is_valid(password)
        voter.set_password(password)
        voter.save()

        return voter
