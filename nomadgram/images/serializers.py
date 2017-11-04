from rest_framework import serializers

from nomadgram.images.models import Comment
from nomadgram.images.models import Image
from nomadgram.images.models import Like
from nomadgram.users.models import User


class FeedUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'profile_image']


class CommentSerializer(serializers.ModelSerializer):

    creator = FeedUserSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'message', 'creator']


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):

    creator = FeedUserSerializer()
    comments = CommentSerializer(many=True)

    class Meta:
        model = Image
        fields = ('id', 'creator', 'file', 'location', 'caption', 'comments', 'like_count')
