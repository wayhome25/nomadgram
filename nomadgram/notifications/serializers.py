from rest_framework import serializers

from nomadgram.images.serializers import CommentSerializer
from nomadgram.images.serializers import SmallImageSerializer
from nomadgram.notifications.models import Notification
from nomadgram.users.serializer import ListUserSerializer


class NotificationSerializer(serializers.ModelSerializer):

    creator = ListUserSerializer()
    image = SmallImageSerializer()
    comment = CommentSerializer()

    class Meta:
        model = Notification
        fields = '__all__'
