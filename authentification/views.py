from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authentification.serializers import VoterSerializer


class RegisterView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VoterSerializer(data=request.data)

        print(request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return HttpResponse("<h1>test<h1>")


class TestView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"msg":"je te cheb"}, status=status.HTTP_200_OK)