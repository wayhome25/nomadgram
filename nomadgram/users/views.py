from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404

from nomadgram.notifications.models import Notification
from nomadgram.users.models import User
from nomadgram.users.serializer import ListUserSerializer
from nomadgram.users.serializer import UserProfileSerializer


class ExploreUsersView(APIView):
    """최근 가입한 유저 리스트를 리턴한다."""
    def get(self, request):
        users = User.objects.all().order_by('-date_joined')[:5]
        serializer = ListUserSerializer(users, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class FollowUser(APIView):

    def post(self, request, user_id):
        user = request.user
        user_to_follow = get_object_or_404(User, id=user_id)
        user.following.add(user_to_follow)

        Notification.objects.create(creator=user, to=user_to_follow,
                                    notificaiton_type=Notification.NotificationType.FOLLOW)

        return Response(status=status.HTTP_200_OK)


class UnFollowUser(APIView):

    def post(self, request, user_id):
        user = request.user
        user_to_unfollow = get_object_or_404(User, id=user_id)
        user.following.remove(user_to_unfollow)

        return Response(status=status.HTTP_200_OK)


class UserProfile(APIView):

    def get(self, request, username):
        query = get_object_or_404(User.objects.prefetch_related('images__comments', 'images__likes'), username=username)
        serializer = UserProfileSerializer(query)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, username):
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

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = ListUserSerializer(user.followers.all(), many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserFollowing(APIView):

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = ListUserSerializer(user.following.all(), many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class Search(APIView):

    def get(self, request):
        username = request.query_params.get('username', None)
        if username:
            found_users = User.objects.filter(username__istartswith=username)
            serializer = ListUserSerializer(found_users, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ChangePassword(APIView):

    def put(self, request, username):
        user = request.user
        if user.username == username:
            current_password = request.data.get('current_password', None)
            if user.check_password(current_password):
                new_password = request.data.get('new_password', None)
                if new_password:
                    user.set_password(new_password)
                    user.save()
                    return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
