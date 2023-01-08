from django.test import TestCase, Client
from .models import User, Post


class CreatePostTestCase(TestCase):

    def setUp(self):

        # Create Dummy User
        user = User.objects.create(username='TestUser')

        # Create Dummy Post
        post = Post.objects.create(
            owner=user, content='This is a test content')

    def test_user_posts_count(self):
        u = User.objects.get(username='TestUser')
        self.assertEqual(u.posts.count(), 1)

    def test_assign_owner(self):
        p = Post.objects.get(content='This is a test content')
        u = User.objects.get(username='TestUser')
        self.assertTrue(p.owner, u)

    def test_post_valid_likes(self):
        p = Post.objects.get(content = 'This is a test content')
        self.assertTrue(p.likes >= 0)
    
    def test_index(self):
        c = Client()
        response = c.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["posts"].count(), 1)
    
    