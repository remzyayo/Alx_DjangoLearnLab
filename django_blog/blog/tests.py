from django.test import TestCase
from django.urls import reverse
from .models import Post

class TagAndSearchTests(TestCase):
    def setUp(self):
        self.p1 = Post.objects.create(title='Apple harvest', slug='apple', content='About apples')
        self.p2 = Post.objects.create(title='Banana things', slug='banana', content='Banana content')
        # add tags using taggit
        self.p1.tags.add('fruit', 'harvest')
        self.p2.tags.add('fruit', 'tropical')

    def test_posts_by_tag(self):
        url = reverse('blog:posts_by_tag', kwargs={'tag_name': 'fruit'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        posts = list(response.context['posts'])
        # both posts should appear
        self.assertIn(self.p1, posts)
        self.assertIn(self.p2, posts)

    def test_search_title(self):
        response = self.client.get(reverse('blog:search_posts') + '?q=Apple')
        self.assertContains(response, self.p1.title)
        self.assertNotContains(response, self.p2.title)

    def test_search_tag(self):
        response = self.client.get(reverse('blog:search_posts') + '?q=harvest')
        self.assertContains(response, self.p1.title)


