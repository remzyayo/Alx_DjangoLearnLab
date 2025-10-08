
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from posts.models import Post

User = get_user_model()

class FollowFeedTests(APITestCase):
    def setUp(self):
        self.u1 = User.objects.create_user(username='u1', password='pass1')
        self.u2 = User.objects.create_user(username='u2', password='pass2')
        self.u3 = User.objects.create_user(username='u3', password='pass3')

        # create posts for u2 and u3
        Post.objects.create(author=self.u2, content='Hello from u2')
        Post.objects.create(author=self.u3, content='Hello from u3')
        Post.objects.create(author=self.u2, content='Another from u2')

    def test_follow_unfollow_and_feed(self):
        # login as u1
        self.client.login(username='u1', password='pass1')

        follow_url = reverse('accounts:follow-user', args=[self.u2.id])
        resp = self.client.post(follow_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(self.u1.is_following(self.u2))

        # feed should include u2 posts
        feed_url = reverse('posts:feed')
        resp = self.client.get(feed_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        # If no pagination, expect list of posts:
        self.assertTrue(any('Hello from u2' in p['content'] for p in data))

        # unfollow
        unfollow_url = reverse('accounts:unfollow-user', args=[self.u2.id])
        resp = self.client.post(unfollow_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertFalse(self.u1.is_following(self.u2))

        # feed should no longer include u2 posts
        resp = self.client.get(feed_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        # depending on pagination serializer, ensure no u2 posts
        self.assertFalse(any(p['author']['username'] == 'u2' for p in data))