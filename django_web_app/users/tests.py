from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post

class BlogTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.post = Post.objects.create(title='Test Post', content='This is a test post.', author=self.user)

    def test_home_view(self):
        response = self.client.get(reverse('blog-home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/home.html')

    def test_post_detail_view(self):
        response = self.client.get(reverse('post-detail', args=[str(self.post.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')
        self.assertContains(response, 'Test Post')

    def test_post_create_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('post-create'), {'title': 'New Post', 'content': 'This is a new post.'})
        self.assertEqual(response.status_code, 302)  # 302 is the HTTP status code for a redirect (success)
        self.assertEqual(Post.objects.count(), 2)  # Assuming you have only one post initially

    def test_post_update_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('post-update', args=[str(self.post.id)]), {'title': 'Updated Post'})
        self.assertEqual(response.status_code, 302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Post')

    def test_post_delete_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('post-delete', args=[str(self.post.id)]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 0)  # Assuming you have only one post initially

    def test_search_view(self):
        response = self.client.get(reverse('search'), {'q': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/home.html')
        self.assertContains(response, 'Test Post')

    # Add more tests as needed for your views and functionalities
