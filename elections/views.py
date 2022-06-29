import datetime
import json
import uuid
from datetime import date

from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from django.shortcuts import render
from django.template import Context
from django.template.loader import get_template
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authentification.models import Voter
from elections.models import Election, Vote, Candidate, Round


class ElectionsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        elections = Election.objects.all()

        data = {}

        for election in elections:
            data[election.election_id] = election.type.__str__()

        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        elections = Election.objects.all()

        print(request.POST)

        query_elections = []

        # if a user parameter was sent in the request, we only send the elections in which
        # the user has the permission to vote in
        if 'electoral_number' in request.POST:
            voter = Voter.objects.all().get(voter_id=request.data["electoral_number"])
            for election in elections:
                if voter.permissions.filter(type_id=election.type.type_id).exists():
                    query_elections.append(election)

            # for election in query_elections:
            #     for rnd in election.progress.all():
            #         if voter.votes.contains(rnd):
            #             query_elections.remove(election)

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


class ElectionNearest(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        token = request.auth.key

        if not token:
            return JsonResponse(
                {"error": "The authentication token provided does not correspond to any known user"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user_id = Token.objects.get(key=token).user_id
        user = Voter.objects.get(voter_id=user_id)

        allowed_election_types = user.permissions.all()

        # tricky line returning all the different elections by type
        all_elections = [election for election in (Election.objects.all().filter(type=election_type).all() for election_type in allowed_election_types)]

        current_date = date.today()
        dates = []

        for elections in all_elections:
            for election in elections:
                for rnd in election.progress.all():
                    dates.append(rnd.date)

        selected_date = datetime.date(2020, 12, 12)

        for dat in dates:
            if dat < current_date:
                continue

            if (dat - current_date) < (selected_date - current_date):
                selected_date = dat

        selected_round = Round.objects.all().get(date)

        if not selected_round:
            return JsonResponse(
                {"error": f"No round found for date {selected_date}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return JsonResponse(
            {"msg": selected_round.__str__()},
            status=status.HTTP_200_OK
        )


class VoteCreationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        body = request.data
        election = Election.objects.get(election_id=body['election_id'])

        if not election:
            return JsonResponse(
                {"error": f'The election of id {body["election_id"]} does not exist'},
                status=status.HTTP_400_BAD_REQUEST
            )

        token = request.auth.key

        if not token:
            return JsonResponse(
                {"error": "The authentication token provided does not correspond to any known user"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user_id = Token.objects.get(key=token).user_id
        user = Voter.objects.get(voter_id=user_id)

        if user:
            if not user.permissions.filter(type_id=election.type.type_id).exists():
                return JsonResponse(
                    {"error": f'tried to cast a vote without '
                              f'the authorization for election {election.__str__()}'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        candidate = Candidate.objects.get(candidate_id=body['candidate_id'])

        if not candidate:
            return JsonResponse(
                {"error": f'the candidate of id {body["candidate_id"]} does not exist'},
                status=status.HTTP_400_BAD_REQUEST
            )

        rnd = Round.objects.get(round_id=body['round_id'])

        # user should not be able to cast a vote in a round that doesn't correspond to the election
        # he wants to vote in
        if not rnd or not election.progress.get(round_id=rnd.round_id):
            return JsonResponse(
                {"error": f'the election of id {body["election_id"]} is not linked'
                          f' with round of id {body["round_id"]}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if user.votes.count() != 0 and user.votes.contains(rnd):
            return JsonResponse(
                {"error": f'the voter of id {user.voter_id} has already cast a vote '
                          f'for round of id {rnd.round_id}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            user.votes.add(rnd.round_id)

        new_vote = Vote.objects.create(
            vote_id=uuid.uuid4(),
            candidate_id=body['candidate_id']
        )
        new_vote.submissions.add(body["round_id"])
        new_vote.save()

        htmly = get_template('vote_casted_email.html')

        subject, from_email, to = 'Merci pour votre vote !', 'app.quetzal@gmail.com', user.email
        html_content = htmly.render(locals())
        msg = EmailMultiAlternatives(subject, "", from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return render(request, 'vote_casted_email.html', locals())


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
                "candidate_photo": candidate.candidate_photo,
                "party": candidate.party.name,
                "party_picture": candidate.party.logo,
                "party_website": candidate.party.website,
                "candidate_id": candidate.candidate_id
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
        candidate = all_candidates.filter(candidate_id=candidate_id).first()

        if not candidate.elections.filter(election_id=election_id).exists():
            return Response({
                "error": f'No candidate with id {candidate_id} for election {election_id}'
            }, status=status.HTTP_400_BAD_REQUEST)

        data = {
            "last_name": candidate.last_name,
            "first_name": candidate.first_name,
            "party": candidate.party.name,
            "party_picture": candidate.party.logo,
            "party_website": candidate.party.website,
            "candidate_id": candidate.candidate_id,
            "candidate_photo": candidate.candidate_photo
        }

        return Response(data, status=status.HTTP_200_OK)
