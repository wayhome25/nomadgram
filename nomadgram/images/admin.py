from django.contrib import admin

from nomadgram.images.models import Comment
from nomadgram.images.models import Image
from nomadgram.images.models import Like


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['file', 'location', 'caption', 'creator', 'created_at', 'updated_at']
    list_display_links = ['file', 'location']
    list_filter = ['location', 'creator']
    search_fields = ['location', 'caption']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['message', 'creator', 'image', 'created_at', 'updated_at']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['creator', 'image', 'created_at', 'updated_at']

