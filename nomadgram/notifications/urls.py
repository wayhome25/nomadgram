from django.conf.urls import url

from nomadgram.notifications import views

# url : /notifications/, namespace : notifications
urlpatterns = [
    url(r'^$', views.Notifications.as_view(), name='notifications'),
]
