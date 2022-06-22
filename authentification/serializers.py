import re
import uuid

from djoser.serializers import UserCreateSerializer

from authentification.validators import is_valid
from django.contrib.auth import password_validation
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from authentification.models import Voter
import regex


class VoterSerializer(UserCreateSerializer):

    email = serializers.EmailField()
    electoral_number = serializers.IntegerField()
    last_name = serializers.CharField(max_length=200)
    first_name = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=200)
    voter_id = serializers.UUIDField(default=uuid.uuid4())

    class Meta(UserCreateSerializer.Meta):
        model = Voter
        fields = (
            'email',
            'electoral_number',
            'last_name',
            'first_name',
            'password',
            'voter_id',
            'username'
        )

    def save(self, **kwargs):
        voter = Voter(
            voter_id=uuid.uuid4(),
            email=self.validated_data['email'],
            last_name=self.validated_data['last_name'],
            first_name=self.validated_data['first_name'],
            electoral_number=self.validated_data['electoral_number'],
            username=self.validated_data['last_name'] + self.validated_data['first_name']
        )

        password = (self.validated_data['password'])

        if is_valid(password):
            voter.set_password(password)
            voter.save()

        return voter
