from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Notification
from django.urls import reverse

User = get_user_model()

class NotificationsTest(APITestCase):
    def setUp(self):
        self.u1 = User.objects.create_user(username='u1', password='pass1')
        self.u2 = User.objects.create_user(username='u2', password='pass2')
        Notification.objects.create(recipient=self.u1, actor=self.u2, verb='followed you')

    def test_list_notifications(self):
        self.client.login(username='u1', password='pass1')
        resp = self.client.get(reverse('notifications:notifications-list'))
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        # if paginated, check results key; but default ListAPIView returns list
        self.assertTrue(len(data) >= 1)


