from django.urls import path

from elections.views import *

urlpatterns = [
    path("", ElectionsView.as_view(), name='see all elections'),
    path("/<int:election_id>", ElectionInfoView.as_view(), name='election info'),
    path("/votes", VoteCreationView.as_view(), name='vote creation'),
    path("/<int:election_id>/candidates", CandidatesView.as_view(), name='see all candidates'),
    path("/<int:election_id>/candidates/<int:candidate_id>", CandidateInfoView.as_view(), name='candidate info')
]