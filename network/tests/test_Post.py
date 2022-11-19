from django.test import TestCase
from ..models import User, Post

# Create your tests here.

class PostTestCase(TestCase):

    def setUp(self):
        user1 = User.objects.create(username='user1')
        user2 = User.objects.create(username='user2')
        user3 = User.objects.create(username='user3')
        user4 = User.objects.create(username='user4')
        Post.objects.create(content='Test post 1', poster=user1)

    def test_getLikes(self):
        """ test get_likes function """
        post1 = Post.objects.get(content='Test post 1')

        self.assertEqual(post1.get_likes(), 0)

    def testLikes(self):
        """ Test likes"""
        user1 = User.objects.get(username='user1')
        user2 = User.objects.get(username='user2')

        post1 = Post.objects.get(poster=user1)
        post1.like(user1)
        post1.like(user2)

        self.assertEqual(post1.get_likes(), 2)

    def testUnlikes(self):
        """ Test likes and unlikes """
        user1 = User.objects.get(username='user1')
        user2 = User.objects.get(username='user2')
        user3 = User.objects.get(username='user3')
        user4 = User.objects.get(username='user4')
        post1 = Post.objects.get(poster=user1)
        post1.like(user1)
        post1.like(user2)
        post1.like(user3)
        post1.like(user4)

        post1.unlike(user1)
        post1.unlike(user2)

        self.assertEqual(post1.get_likes(), 2)

    def testLikers(self):
        """ Test what happens to a post when its liker is deleted."""
        user1 = User.objects.get(username='user1')
        user2 = User.objects.get(username='user2')
        post1 = Post.objects.get(poster=user1)
        
        post1.like(user2)
        user2.delete()

        self.assertEqual(post1.get_likes(), 0)

    def testLikeRedundancy(self):
        """ Test what happens when a user likes the post several times """
        user1 = User.objects.get(username='user1')
        user2 = User.objects.get(username='user2')
        post1 = Post.objects.get(poster=user1)

        post1.like(user2)
        post1.like(user2)
        post1.like(user2)

        self.assertEqual(post1.get_likes(), 1)

    def testUnlikeRedundancy(self):
        """ Test what happens when a user unlikes the post several times """
        user1 = User.objects.get(username='user1')
        user2 = User.objects.get(username='user2')
        post1 = Post.objects.get(poster=user1)

        post1.like(user2)

        post1.unlike(user2)
        post1.unlike(user2)
        post1.unlike(user2)

        self.assertEqual(post1.get_likes(), 0)