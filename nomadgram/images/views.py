from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.db.models import Q
from django.shortcuts import get_object_or_404

from nomadgram.images.models import Comment
from nomadgram.images.models import Image
from nomadgram.images.models import Like
from nomadgram.images.serializers import CommentSerializer
from nomadgram.images.serializers import CountImageSerializer
from nomadgram.images.serializers import ImageSerializer
from nomadgram.notifications.models import Notification


class Feed(APIView):

    def get(self, request, format=None):
        user = request.user
        following_users = user.following.all()
        feed_images = Image.objects.filter(Q(creator__in=following_users) | Q(creator=user))[:3]
        serializer = ImageSerializer(feed_images, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ImageDetail(APIView):

    def get(self, request, image_id, format=None):
        image = get_object_or_404(Image, id=image_id)
        serializer = ImageSerializer(image)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class LikeImage(APIView):

    def post(self, request, image_id, format=None):
        user = request.user
        image = get_object_or_404(Image, id=image_id)

        try:
            Like.objects.get(creator=user, image=image)
            return Response(status=status.HTTP_304_NOT_MODIFIED)

        except Like.DoesNotExist:
            Like.objects.create(creator=user, image=image)  # NOTE(다른방법): image.likes.create(creator=user)
            Notification.objects.create(creator=user, to=image.creator, notificaiton_type='like', image=image)
            return Response(status=status.HTTP_201_CREATED)


class UnLikeImage(APIView):

    def delete(self, request, image_id, format=None):
        user = request.user
        image = get_object_or_404(Image, id=image_id)

        try:
            preexisting_like = Like.objects.get(creator=user, image=image)
            preexisting_like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Like.DoesNotExist:
            return Response(status=status.HTTP_304_NOT_MODIFIED)


class CommentOnImage(APIView):

    def post(self, request, image_id, format=None):
        user = request.user
        image = get_object_or_404(Image, id=image_id)

        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            comment = serializer.save(creator=user, image=image)  # NOTE: serializer.save() 는 모델 인스턴스를 리턴
            Notification.objects.create(creator=user, to=image.creator, notificaiton_type='comment', image=image,
                                        comment=comment)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentView(APIView):

    def delete(self, request, comment_id, format=None):
        user = request.user
        comment = get_object_or_404(Comment, id=comment_id, creator=user)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ModerateComments(APIView):

    def delete(self, request, image_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id, image_id=image_id, image__creatorgs=request.user)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Search(APIView):

    def get(self, request, format=None):
        tags = request.query_params.get('tags', None)  # NOTE: query_params 를 통해서 query string을 가져온다.
        if tags:
            tags = tags.split(',')
            images = Image.objects.filter(tags__name__in=tags).distinct()
            serializer = CountImageSerializer(images, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
