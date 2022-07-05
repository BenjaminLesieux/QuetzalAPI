import requests
from django.http import HttpResponseRedirect
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response


@permission_classes('AllowAny', )
@api_view(('GET',))
def activation_view(request, uid, token):
    requests.post("https://voteatquetzal.herokuapp.com/api/v1/users/activation/",
                  json={
                      "uid": uid,
                      "token": token
                  })
    return HttpResponseRedirect(request.GET.get('https://vote-quetzal.herokuapp.com/activated'))


@permission_classes('AllowAny', )
@api_view(('GET',))
def reset_password_view(request, email):
    requests.post("https://voteatquetzal.herokuapp.com/api/v1/users/reset_password/",
                  json={
                      "email": email,
                  })
    return Response({'msg': 'you can change your password'}, status=status.HTTP_200_OK)


@permission_classes('AllowAny', )
@api_view(('GET',))
def redirect_password_change(request, uid, token):
    return HttpResponseRedirect(redirect_to=f'https://vote-quetzal.herokuapp.com/reinitialisation/{uid}/{token}')

