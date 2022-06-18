from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView


class VoteCreationView(APIView):

    permission_classes = [TokenAuthentication]

    def post(self, request):
        pass

    def get(self, request, elections_id, round_id, candidate_id):
        print(elections_id + " " + round_id + " " + candidate_id)
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
