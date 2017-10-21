from rest_framework.views import APIView
from rest_framework.response import Response

from nomadgram.images.models import Image, Comment, Like
from nomadgram.images.serializers import ImageSerializer, CommentSerializer, LikeSerializer


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
