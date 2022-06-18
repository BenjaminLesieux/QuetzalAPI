from django.urls import path

from elections.views import VoteCreationView

urlpatterns = [
    path('api/v1/elections/<uuid:elections_id>/<uuid:round_id>/vote/candidates/<int:candidate_id>',
         VoteCreationView.as_view(),
         name='vote creation'
         )
]