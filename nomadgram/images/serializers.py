from rest_framework import serializers

from nomadgram.images.models import Comment
from nomadgram.images.models import Image
from nomadgram.images.models import Like


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):

    comments = CommentSerializer(many=True)
    likes = LikeSerializer(many=True)

    class Meta:
        model = Image
        fields = ('id', 'file', 'location', 'caption', 'comments', 'likes')
