from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404

from nomadgram.users.models import User
from nomadgram.users.serializer import ListUserSerializer
from nomadgram.users.serializer import UserProfileSerializer


class ExploreUsers(APIView):

    def get(self, request, format=None):
        users = User.objects.all().order_by('-date_joined')[:5]
        serializer = ListUserSerializer(users, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class FollowUser(APIView):

    def post(self, request, user_id, format=None):
        user = request.user
        user_to_follow = get_object_or_404(User, id=user_id)
        user.following.add(user_to_follow)

        return Response(status=status.HTTP_200_OK)


class UnFollowUser(APIView):

    def post(self, request, user_id, format=None):
        user = request.user
        user_to_unfollow = get_object_or_404(User, id=user_id)
        user.following.remove(user_to_unfollow)

        return Response(status=status.HTTP_200_OK)


class UserProfile(APIView):

    def get(self, request, username, format=None):
        user = get_object_or_404(User, username=username)
        serializer = UserProfileSerializer(user)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserFollowers(APIView):

    def get(self, request, username, format=None):
        user = get_object_or_404(User, username=username)
        serializer = ListUserSerializer(user.followers.all(), many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserFollowing(APIView):

    def get(self, request, username, format=None):
        user = get_object_or_404(User, username=username)
        serializer = ListUserSerializer(user.following.all(), many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
