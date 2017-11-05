from rest_framework import serializers

from nomadgram.users.models import User


class ExploreUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['profile_image', 'username', 'name']
