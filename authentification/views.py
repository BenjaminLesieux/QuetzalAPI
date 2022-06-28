import requests
from django.http import HttpResponseRedirect
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response


@permission_classes('AllowAny', )
@api_view(('GET',))
def activation_view(request, uid, token):
    requests.post("http://10.13.200.195:8000/api/v1/users/activation/",
                  json={
                      "uid": uid,
                      "token": token
                  })
    return HttpResponseRedirect(request.GET.get('http://10.13.216.93:8081/reinitialisation'))


@permission_classes('AllowAny', )
@api_view(('GET',))
def test_view(request):
    print("here")
    return HttpResponseRedirect(redirect_to='http://10.13.216.93:8081/reinitialisation')

