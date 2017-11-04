from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.db.models import Q
from django.shortcuts import get_object_or_404

from nomadgram.images.models import Image
from nomadgram.images.models import Like
from nomadgram.images.serializers import CommentSerializer
from nomadgram.images.serializers import ImageSerializer


class Feed(APIView):

    def get(self, request, format=None):
        user = request.user
        following_users = user.following.all()
        feed_images = Image.objects.filter(Q(creator__in=following_users) | Q(creator=user))[:2]
        serializer = ImageSerializer(feed_images, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class LikeImage(APIView):

    def get(self, request, image_id, format=None):
        user = request.user
        image = get_object_or_404(Image, id=image_id)

        try:
            preexisting_like = Like.objects.get(creator=user, image=image)
            preexisting_like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Like.DoesNotExist:
            Like.objects.create(creator=user, image=image)  # NOTE(다른방법): image.likes.create(creator=user)

        return Response(status=status.HTTP_201_CREATED)


class CommentOnImage(APIView):

    def post(self, request, image_id, format=None):
        user = request.user
        image = get_object_or_404(Image, id=image_id)

        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(creator=user, image=image)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
