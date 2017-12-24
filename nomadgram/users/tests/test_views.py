from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate

from nomadgram.users.tests.factories import UserFactory
from nomadgram.users.views import ExploreUsersView


class ExploreUsersViewTestCase(APITestCase):

    def setUp(self):
        factory = APIRequestFactory()
        self.request = factory.get(reverse('users:explore_users'))
        self.view = ExploreUsersView.as_view()
        self.user = UserFactory()

    def test_get_미로그인_상태에서_401_리턴(self):
        response = self.view(self.request)

        self.assertEqual(response.status_code, 401)

    def test_get_로그인_상태에서_200_리턴(self):
        force_authenticate(self.request, user=self.user)
        response = self.view(self.request)

        self.assertEqual(response.status_code, 200)

    def test_get_리턴한_유저정보_확인(self):
        force_authenticate(self.request, user=self.user)
        today = timezone.now()
        for i in range(10):
            if i == 0:
                first_user = UserFactory(date_joined=today - timedelta(days=i))
            else:
                UserFactory(date_joined=today - timedelta(days=i))
        response = self.view(self.request)

        self.assertEqual(len(response.data), 5)
        self.assertEqual(response.data[0]["name"], first_user.name)
