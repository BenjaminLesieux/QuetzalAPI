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
