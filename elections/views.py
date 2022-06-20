from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView


class VoteCreationView(APIView):

    permission_classes = [AllowAny]

    def post(self, request, elections_id, round_id):
        pass

    def get(self, request, elections_id, round_id):
        print(elections_id + " " + round_id + " ")
