from rest_framework import serializers

from nomadgram.images.models import Comment
from nomadgram.images.models import Image
from nomadgram.images.models import Like
from nomadgram.users.models import User


class SmallImageSerializer(serializers.ModelSerializer):
    """Used for the notifications"""

    class Meta:
        model = Image
        fields = ['file']


class CountImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ['id', 'file', 'comment_count', 'like_count']


class FeedUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'profile_image']


class CommentSerializer(serializers.ModelSerializer):

    creator = FeedUserSerializer(read_only=True)

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
        fields = ('id', 'creator', 'file', 'location', 'caption', 'comments', 'like_count', 'created_at')


class InputImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ["file", "location", "caption"]
