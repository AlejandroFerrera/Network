from django.test import TestCase, Client
from .models import User, Post


class CreatePostTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username = 'testuser',
            password = 'testpassword'
        )

    def test_user_posts_count(self):
        p = Post.objects.create(content = 'test content', owner = self.user)
        self.assertEqual(self.user.posts.count(), 1)

    def test_assign_owner(self):
        p = Post.objects.create(content='This is a test content', owner = self.user)
        self.assertTrue(p.owner, self.user)
        self.assertTrue(p.content, 'This is a test content')

    def test_post_valid_likes(self):
        p = Post.objects.create(content = 'This is a test content', owner = self.user)
        self.assertTrue(p.likes >= 0)
    
    def test_index(self):
        c = Client()
        p = Post.objects.create(content = '', owner = self.user)
        response = c.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["posts"].count(), 1)
    
    