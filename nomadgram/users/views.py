from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404

from nomadgram.notifications.models import Notification
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

        Notification.objects.create(creator=user, to=user_to_follow, notificaiton_type='follow')

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

    def put(self, request, username, format=None):
        try:
            user = User.objects.get(id=request.user.id, username=username)
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = UserProfileSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(data=serializer.errors, status=status.HTTP_304_NOT_MODIFIED)


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


class Search(APIView):

    def get(self, request, format=None):
        username = request.query_params.get('username', None)
        if username:
            found_users = User.objects.filter(username__istartswith=username)
            serializer = ListUserSerializer(found_users, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
