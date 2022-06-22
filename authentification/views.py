import requests
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.password_validation import validate_password

from authentification.serializers import VoterSerializer


@api_view(('GET',))
def activation_view(request, uid, token):
    requests.post("http://10.3.201.28:8000/api/v1/users/activation/",
                  json={
                      "uid": uid,
                      "token": token
                  })
    return Response({'msg': 'The account was created !'}, status=status.HTTP_200_OK)
