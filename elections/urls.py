from django.urls import path

from elections.views import VoteCreationView

urlpatterns = [
    path('api/v1/elections/<int:elections_id>/<int:round_id>/',
         VoteCreationView.as_view(),
         name='vote creation'
         )
]