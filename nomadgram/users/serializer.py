from rest_framework import serializers

from nomadgram.images.serializers import CountImageSerializer
from nomadgram.users.models import User


class UserProfileSerializer(serializers.ModelSerializer):

    images = CountImageSerializer(many=True)

    class Meta:
        model = User
        fields = ['profile_image', 'username', 'name', 'bio', 'website', 'post_count',
                  'followers_count', 'following_count', 'images']


class ListUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'profile_image', 'username', 'name']
