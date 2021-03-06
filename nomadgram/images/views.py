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
from nomadgram.images.serializers import InputImageSerializer
from nomadgram.notifications.models import Notification
from nomadgram.users.models import User
from nomadgram.users.serializer import ListUserSerializer


class Images(APIView):

    def get(self, request):
        user = request.user
        following_users = user.following.all()
        feed_images = Image.objects.filter(Q(creator__in=following_users) | Q(creator=user))[:3]
        query = feed_images.select_related('creator').prefetch_related('comments__creator', 'tags', 'likes')
        serializer = ImageSerializer(query, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        serializer = InputImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageDetail(APIView):

    def find_own_image(self, image_id, user):
        try:
            image = Image.objects.get(id=image_id, creator=user)
            return image
        except Image.DoesNotExist:
            return None

    def get(self, request, image_id):
        image = get_object_or_404(Image, id=image_id)
        serializer = ImageSerializer(image)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, image_id):
        user = request.user
        image = self.find_own_image(image_id, user)
        if image:
            serializer = InputImageSerializer(image, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save(creator=user)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(data=serializer.erros, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, image_id):
        user = request.user
        image = self.find_own_image(image_id, user)
        if image:
            image.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LikeImage(APIView):

    def get(self, request, image_id):
        """like 유저 리스트를 가져온다"""
        likes = Like.objects.filter(image_id=image_id)
        likes_creator_ids = likes.values('creator_id')
        like_users = User.objects.filter(id__in=likes_creator_ids)

        serializer = ListUserSerializer(like_users, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, image_id):
        """like를 추가한다"""
        user = request.user
        image = get_object_or_404(Image, id=image_id)

        try:
            Like.objects.get(creator=user, image=image)
            return Response(status=status.HTTP_304_NOT_MODIFIED)

        except Like.DoesNotExist:
            Like.objects.create(creator=user, image=image)  # NOTE(다른방법): image.likes.create(creator=user)
            Notification.objects.create(creator=user, to=image.creator, image=image,
                                        notificaiton_type=Notification.NotificationType.LIKE)
            return Response(status=status.HTTP_201_CREATED)


class UnLikeImage(APIView):

    def delete(self, request, image_id):
        user = request.user
        image = get_object_or_404(Image, id=image_id)

        try:
            preexisting_like = Like.objects.get(creator=user, image=image)
            preexisting_like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Like.DoesNotExist:
            return Response(status=status.HTTP_304_NOT_MODIFIED)


class CommentOnImage(APIView):

    def post(self, request, image_id):
        user = request.user
        image = get_object_or_404(Image, id=image_id)

        serializer = CommentSerializer(data=request.POST)

        if serializer.is_valid():
            comment = serializer.save(creator=user, image=image)  # NOTE: serializer.save() 는 모델 인스턴스를 리턴
            Notification.objects.create(creator=user, to=image.creator, image=image, comment=comment,
                                        notificaiton_type=Notification.NotificationType.COMMENT)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentView(APIView):

    def delete(self, request, comment_id):
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

    def get(self, request):
        tags = request.query_params.get('tags', None)  # NOTE: query_params 를 통해서 query string을 가져온다.
        if tags:
            tags = tags.split(',')
            images = Image.objects.filter(tags__name__in=tags).distinct()
            serializer = CountImageSerializer(images, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
