from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.password_validation import validate_password

from authentification.serializers import VoterSerializer


class RegisterView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VoterSerializer(data=request.data)

        if serializer.is_valid():
            return_data = {
                "last_name": request.data['name'],
                "first_name": request.data['surname'],
                "username": request.data['username'],

            }

            voter = serializer.save()
            authenticate(voter)
            return Response(return_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):
        pass