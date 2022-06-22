from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from elections.models import Election


class ElectionsView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        elections = Election.objects.all()
        data = {}

        for election in elections:
            data[election.election_id] = election.type.__str__()

        return Response(data, status=status.HTTP_200_OK)


class ElectionInfoView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, election_id):

        if not Election.objects.filter(election_id=election_id).exists():
            return Response({"error": "the given id does not correspond to any elections in our database"},
                            status=status.HTTP_400_BAD_REQUEST)

        election = Election.objects.get(election_id=election_id)
        rounds = election.progress.all()

        data = {}
        round_counter = 0

        for round in rounds:
            round_counter += 1
            data[f'round_{round_counter}'] = round.__str__()

        return Response({
            "election": election.__str__(),
            "type_information": election.type.__str__(),
        } | data, status=status.HTTP_200_OK)

class VoteCreationView(APIView):

    def post(self):
        pass