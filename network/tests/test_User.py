from django.core.exceptions import ValidationError
from django.test import TestCase
from ..models import User

class UserTestCase(TestCase):
    
    def setUp(self):
        for i in range(0,5):
            User.objects.create(username=f'username{i}')

    def testFollowNumber(self):
        users = []
        for i in range(0,5):
            users.append(User.objects.get(username=f'username{i}'))

        for i in range(1,5):
            users[i].follow(users[0])

        # Some redundancy
        users[1].follow(users[0])
        users[1].follow(users[0])

        self.assertEqual(users[0].get_total_followers(), 4)

    def testUnfollowNumber(self):
        users = []
        for i in range(0,5):
            users.append(User.objects.get(username=f'username{i}'))

        for i in range(1,5):
            users[i].follow(users[0])

        users[1].unfollow(users[0])
        users[2].unfollow(users[0])

        # some redundancy
        users[1].unfollow(users[0])
        users[1].unfollow(users[0])

        self.assertEqual(users[0].get_total_followers(), 2)

    def testNaricssisFollow(self):
        """ Test a user can't follow themself """
        user = User.objects.get(username='username0')

        self.assertRaises(ValidationError, user.follow, user)

    def testDeletedFollower(self):
        """ Test what happens when a follower is deleted """
        user0 = User.objects.get(username='username0')
        user1 = User.objects.get(username='username1')
        
        user1.follow(user0)
        user1.delete()

        self.assertEqual(user0.get_total_followers(), 0)

    def testDeletedFollowed(self):
        """ Test what happens when the user you follow is deleted """
        user0 = User.objects.get(username='username0')
        user1 = User.objects.get(username='username1')
        
        user0.follow(user1)
        user1.delete()

        self.assertEqual(user0.get_total_following(), 0)