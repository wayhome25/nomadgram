from django.conf.urls import url

from nomadgram.users import views

# url: /users/ , namespace: users
urlpatterns = [
    url('^explore/$', views.ExploreUsers.as_view(), name='explore_users'),
]
