from rest_framework import serializers

from nomadgram.images.serializers import SmallImageSerializer
from nomadgram.notifications.models import Notification
from nomadgram.users.serializer import ListUserSerializer


class NotificationSerializer(serializers.ModelSerializer):

    creator = ListUserSerializer()
    image = SmallImageSerializer()

    class Meta:
        model = Notification
        fields = '__all__'
