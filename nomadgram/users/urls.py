from django.conf.urls import url

from nomadgram.users import views

# url: /users/ , namespace: users
urlpatterns = [
    url('^explore/$', views.ExploreUsersView.as_view(), name='explore_users'),
    url('^search/$', views.Search.as_view(), name='user_search'),
    url('^(?P<user_id>\d+)/follow/$', views.FollowUser.as_view(), name='follow_user'),
    url('^(?P<user_id>\d+)/unfollow/$', views.UnFollowUser.as_view(), name='unfollow_user'),
    url('^(?P<username>\w+)/$', views.UserProfile.as_view(), name='user_profile'),
    url('^(?P<username>\w+)/followers/$', views.UserFollowers.as_view(), name='user_followers'),
    url('^(?P<username>\w+)/following/$', views.UserFollowing.as_view(), name='user_following'),
    url('^(?P<username>\w+)/password/$', views.ChangePassword.as_view(), name='change_password'),
    url(r'^login/facebook/$', views.FacebookLogin.as_view(), name='fb_login'),
]
