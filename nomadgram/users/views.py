from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from nomadgram.users.models import User
from nomadgram.users.serializer import ExploreUserSerializer


class ExploreUsers(APIView):

    def get(self, request, format=None):
        users = User.objects.all().order_by('-date_joined')[:5]
        serializer = ExploreUserSerializer(users, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
