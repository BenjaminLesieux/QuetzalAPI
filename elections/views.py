import json
import uuid

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from authentification.models import Voter
from elections.models import Election, Vote, Candidate, Round


class ElectionsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):

        elections = Election.objects.all()

        print(request.POST)

        query_elections = []

        # if a user parameter was sent in the request, we only send the elections in which
        # the user has the permission to vote in
        if 'voter_id' in request.POST:
            voter = Voter.objects.all().get(voter_id=request.data["voter_id"])
            for election in elections:
                if voter.permissions.filter(type_id=election.type.type_id).exists():
                    query_elections.append(election)

        if len(query_elections) != 0:
            elections = query_elections

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

        candidates = Candidate.objects.all()
        election_candidates = []

        for candidate in candidates:
            if candidate.elections.filter(election_id=election_id).exists():
                election_candidates.append(candidate)

        return Response({
                            "election": election.__str__(),
                            "type_information": election.type.__str__(),
                        } | data, status=status.HTTP_200_OK)


class VoteCreationView(APIView):
    permission_classes = [TokenAuthentication]

    def post(self, request):
        body = request.data
        headers = request.META

        new_vote = Vote.objects.create(
            vote_id=uuid.uuid4(),
            candidate_id=body['candidate_id']
        )

        election = Election.objects.all().filter(election_id=body['election_id'])

        if not election.exists():
            return Response(
                {"error": f'The election of id {body["election_id"]} does not exist'}
            )

        user_id = Token.objects.get(key=headers["Authorization"]).user_id
        user = Voter.objects.all().filter(voter_id=user_id)

        if user.exists():
            if not user.first().permissions.filter(type_id=election.type.type_id).exists():
                return Response(
                    {"error": f'tried to cast a vote without '
                              f'the authorization for election {election.first().__str__()}'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        candidate = Candidate.objects.all().filter(candidate_id=body['candidate_id'])

        if not candidate.exists():
            return Response(
                {"error": f'the candidate of id {body["candidate_id"]} does not exist'},
                status=status.HTTP_400_BAD_REQUEST
            )

        rnd = Round.objects.all().filter(round_id=body['round_id'])

        # user should not be able to cast a vote in a round that doesn't correspond to the election
        # he wants to vote in
        if not rnd.exists() and not election.first().progress.filter(round_id=body["round_id"]).exists():
            return Response(
                {"error": f'the election of id {body["election_id"]} is not linked'
                          f' with round of id {body["round_id"]}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        new_vote.submissions.add(body["round_id"])
        new_vote.save()

        return Response(
            {"msg": f'The vote {new_vote.vote_id} has been fully registered of election of id {body["election_id"]}'
                    f' at round {body["round_id"]}'},
            status=status.HTTP_200_OK
        )


class CandidatesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, election_id):

        elections = Election.objects.all()

        if not elections.filter(election_id=election_id).exists():
            return Response(
                {"error": f'No election with this id {election_id} exists'},
                status=status.HTTP_400_BAD_REQUEST
            )

        all_candidates = Candidate.objects.all()
        election_candidates = []

        for candidate in all_candidates:
            if candidate.elections.filter(election_id=election_id).exists():
                election_candidates.append(candidate)

        data = {}

        for candidate in election_candidates:
            data[candidate.candidate_id] = {
                "last_name": candidate.last_name,
                "first_name": candidate.first_name,
                "candidate_photo": candidate.first_name,
                "party": candidate.party.name,
                "party_picture": candidate.party.logo,
                "party_website": candidate.party.website
            }

        return Response(data, status=status.HTTP_200_OK)


class CandidateInfoView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, election_id, candidate_id):
        elections = Election.objects.all()

        if not elections.filter(election_id=election_id).exists():
            return Response(
                {"error": f'No election with this id {election_id} exists'},
                status=status.HTTP_400_BAD_REQUEST
            )

        all_candidates = Candidate.objects.all()
        election_candidates = []

        candidate = all_candidates.filter(candidate_id=candidate_id).first()

        if not candidate.elections.filter(election_id=election_id).exists():
            return Response({
                "error": f'No candidate with id {candidate_id} for election {election_id}'
            }, status=status.HTTP_400_BAD_REQUEST)

        data = {
            "last_name": candidate.last_name,
            "first_name": candidate.first_name,
            "candidate_photo": candidate.first_name,
            "party": candidate.party.name,
            "party_picture": candidate.party.logo,
            "party_website": candidate.party.website
        }

        return Response(data, status=status.HTTP_200_OK)


