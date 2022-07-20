from django.urls import path, include

from authentification import views

urlpatterns = [
   path('', include('djoser.urls.authtoken')),
   path('activate/<uid>/<token>', views.activation_view),
   path('password/reset/confirm/<uid>/<token>', views.redirect_password_change),
]