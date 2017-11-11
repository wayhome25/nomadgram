from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from nomadgram.notifications.models import Notification
from nomadgram.notifications.serializers import NotificationSerializer


class Notifications(APIView):

    def get(self, request, format=None):
        user = request.user
        notifications = Notification.objects.filter(to=user)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
