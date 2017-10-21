from django.conf.urls import url

from nomadgram.images import views

urlpatterns = [
    url(r'^all/$', views.ListAllImages.as_view(), name='all')
]
