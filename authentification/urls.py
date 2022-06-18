from django.urls import path, include

from authentification.views import RegisterView

urlpatterns = [
   path('register/', RegisterView.as_view(), name='register'),
   path('', include('djoser.urls.authtoken'))
]