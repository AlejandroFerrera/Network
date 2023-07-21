from django.test import TestCase, Client
from django.urls import reverse
from .models import Post, User

class NetworkTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.post = Post.objects.create(
            owner=self.user, content='test post')

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'network/pages/index.html')
        self.assertContains(response, self.post.content)

    def test_login_view(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

    def test_register_view(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass',
            'confirmation': 'newpass'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_create_post(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('index'), {
            'new_post_content': 'new post'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'new post')
        self.assertTrue(Post.objects.filter(content='new post').exists())