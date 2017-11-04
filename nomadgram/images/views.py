from rest_framework.response import Response
from rest_framework.views import APIView

from nomadgram.images.models import Comment
from nomadgram.images.models import Image
from nomadgram.images.models import Like
from nomadgram.images.serializers import CommentSerializer
from nomadgram.images.serializers import ImageSerializer
from nomadgram.images.serializers import LikeSerializer


class ListAllImages(APIView):

    def get(self, request, format=None):
        all_images = Image.objects.all()
        serializer = ImageSerializer(all_images, many=True)
        return Response(data=serializer.data)


class ListAllComments(APIView):

    def get(self, request, format=None):
        all_comments = Comment.objects.all()
        serializer = CommentSerializer(all_comments, many=True)
        return Response(data=serializer.data)


class ListAllLikes(APIView):

    def get(self, request, format=None):
        all_likes = Like.objects.all()
        serializer = LikeSerializer(all_likes, many=True)
        return Response(data=serializer.data)
