from pdb import post_mortem
from django.test import TestCase
from .models import User, Post

# Create your tests here.

class PostTestCase(TestCase):

    def setUp(self):
        user1 = User.objects.create(username='user1')
        user2 = User.objects.create(username='user2')
        user3 = User.objects.create(username='user3')
        user4 = User.objects.create(username='user4')
        Post.objects.create(content='Test post 1', poster=user1)
    
    def testLikes(self):
        """ Test likes number """
        user1 = User.objects.get(username='user1')
        user2 = User.objects.get(username='user2')
        # user3 = User.objects.get(username='user3')
        # user4 = User.objects.get(username='user4')
        post1 = Post.objects.get(poster=user1)

        post1.like(user1)
        post1.like(user2)
        # post1.like(user3)
        # post1.like(user4)
        post1.like(user1)
        post1.like(user1)
        post1.like(user1)
        post1.like(user1)

        self.assertEqual(post1.likes, 2)

    def testLikers(self):
        """ Test likers array """
        user1 = User.objects.get(username='user1')
        user2 = User.objects.get(username='user2')
        # user3 = User.objects.get(username='user3')
        # user4 = User.objects.get(username='user4')
        post1 = Post.objects.get(poster=user1)
        post1.like(user1)
        post1.like(user2)
        # post1.like(user3)
        # post1.like(user4)
        post1.like(user1)
        post1.like(user1)
        post1.like(user1)

        self.assertEqual(post1.likers.all().count(), 2)

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

        # Some redundancy
        post1.like(user1)
        post1.like(user1)

        post1.unlike(user1)
        post1.unlike(user2)

        # Some unlike redundancy
        post1.unlike(user2)
        post1.unlike(user1)
        post1.unlike(user1)

        self.assertEqual(post1.likes, 2)