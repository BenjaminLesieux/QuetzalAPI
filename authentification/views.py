import requests
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response


@permission_classes('AllowAny', )
@api_view(('GET',))
def activation_view(request, uid, token):
    requests.post("http://10.3.201.28:8000/api/v1/users/activation/",
                  json={
                      "uid": uid,
                      "token": token
                  })
    return Response({'msg': 'The account was created !'}, status=status.HTTP_200_OK)


@permission_classes('AllowAny', )
@api_view(('GET',))
def reset_password_validation_view(request, uid, token):
    requests.post("http://10.3.201.28:8000/api/v1/users/reset_password_confirm/",
                  json={
                      "new_password": request.data["new_password"],
                      "re_new_password": request.data["re_new_password"],
                      "uid": uid,
                      "token": token
                  })
    return Response({'msg': 'Your password has been changed'}, status=status.HTTP_200_OK)


@permission_classes('AllowAny', )
@api_view(('GET',))
def reset_password_view(request, email):
    requests.post("http://10.13.216.11:8000/api/v1/users/reset_password/",
                  json={
                      "email": email,
                  })
    return Response({'msg': 'you can change your password'}, status=status.HTTP_200_OK)
