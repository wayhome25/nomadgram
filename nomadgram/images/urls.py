from django.conf.urls import url

from nomadgram.images import views

# url : /images/, namespace : images
urlpatterns = [
    url(r'^$', views.Feed.as_view(), name='feed'),
    url(r'^(?P<image_id>\d+)/likes/$', views.LikeImage.as_view(), name='like_image'),
    url(r'^(?P<image_id>\d+)/comments/$', views.CommentOnImage.as_view(), name='comment_image'),
    url(r'^comments/(?P<comment_id>\d+)/$', views.CommentView.as_view(), name='comment'),
]
