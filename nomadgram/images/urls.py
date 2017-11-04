from django.conf.urls import url

from nomadgram.images import views

# url : /images/, namespace : images
urlpatterns = [
    url(r'^all/$', views.ListAllImages.as_view(), name='all_images'),
    url(r'^comments/$', views.ListAllComments.as_view(), name='all_comments'),
    url(r'^likes/$', views.ListAllLikes.as_view(), name='all_likes'),
]
