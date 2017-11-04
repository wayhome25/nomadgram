from django.conf.urls import url

from nomadgram.images import views

# url : /images/, namespace : images
urlpatterns = [
    url(r'^$', views.Feed.as_view(), name='feed'),
    url(r'^(?P<image_id>\d+)/like/$', views.LikeImage.as_view(), name='like_image'),
    url(r'^(?P<image_id>\d+)/comment/$', views.CommentOnImage.as_view(), name='comment_image'),
]
