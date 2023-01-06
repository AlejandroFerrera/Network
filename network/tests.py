from django.test import TestCase
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

    def test_post_owner_count(self):
        p = Post.objects.get(content='This is a test content')
        self.assertTrue(p.owner, 'No puede tener mas de un dueño el post')

    def test_post_valid_likes(self):
        p = Post.objects.get(content = 'This is a test content')
        self.assertTrue(p.likes >= 0)
    
    
