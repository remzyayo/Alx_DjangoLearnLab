from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from .models import Post, Like
from notifications.models import Notification

User = get_user_model()

class LikesNotificationsTest(APITestCase):
    def setUp(self):
        self.u1 = User.objects.create_user(username='u1', password='pass1')
        self.u2 = User.objects.create_user(username='u2', password='pass2')
        self.post = Post.objects.create(author=self.u2, content='Hello')

    def test_like_creates_like_and_notification(self):
        self.client.login(username='u1', password='pass1')
        like_url = reverse('posts:like-post', args=[self.post.pk])
        resp = self.client.post(like_url)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Like.objects.filter(user=self.u1, post=self.post).exists())
        # notification to post author
        notif_exists = Notification.objects.filter(recipient=self.u2, actor=self.u1, verb__icontains='like').exists()
        self.assertTrue(notif_exists)

    def test_unlike_removes_like_and_notification(self):
        self.client.login(username='u1', password='pass1')
        # like first
        self.client.post(reverse('posts:like-post', args=[self.post.pk]))
        # unlike
        resp = self.client.post(reverse('posts:unlike-post', args=[self.post.pk]))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertFalse(Like.objects.filter(user=self.u1, post=self.post).exists())


