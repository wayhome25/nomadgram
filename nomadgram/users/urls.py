from django.conf.urls import url

from nomadgram.users import views

# url: /users/ , namespace: users
urlpatterns = [
    url('^explore/$', views.ExploreUsers.as_view(), name='explore_users'),
    url('^(?P<user_id>\d+)/follow/$', views.FollowUser.as_view(), name='follow_user'),
    url('^(?P<user_id>\d+)/unfollow/$', views.UnFollowUser.as_view(), name='unfollow_user'),
    url('^(?P<username>\w+)/$', views.UserProfile.as_view(), name='user_profile'),
    url('^(?P<username>\w+)/followers/$', views.UserFollowers.as_view(), name='user_followers'),
    url('^(?P<username>\w+)/following/$', views.UserFollowing.as_view(), name='user_following')
]

# /users/12/follow/
