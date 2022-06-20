from django.urls import path

from elections.views import ElectionsView, ElectionInfoView

urlpatterns = [
    path("", ElectionsView.as_view(), name='see all elections'),
    path("/<int:election_id>", ElectionInfoView.as_view(), name='election info')
]