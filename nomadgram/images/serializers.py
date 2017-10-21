from rest_framework import serializers

from nomadgram.images.models import Comment
from nomadgram.images.models import Image
from nomadgram.images.models import Like


class ImageSerializer(serializers.Serializer):

    class Meta:
        model = Image
        fields = '__all__'


class CommentSerializer(serializers.Serializer):

    class Meta:
        model = Comment
        fields = '__all__'


class LikeSerializer(serializers.Serializer):

    class Meta:
        models = Like
        fields = '__all__'
