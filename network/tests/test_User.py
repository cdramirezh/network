from django.test import TestCase
from ..models import User

class UserTestCase(TestCase):
    
    def setUp(self):
        for i in range(0,5):
            User.objects.create(username=f'username${i}')

    def testFollowNumber(self):
        users = []
        for i in range(0,5):
            users.append(User.objects.get(username=f'username${i}'))

        for i in range(1,5):
            users[i].follow(users[0])

        # Some redundancy
        users[1].follow(users[0])
        users[1].follow(users[0])

        self.assertEqual(users[0].followers.all().count(), 4)

    def testUnfollowNumber(self):
        users = []
        for i in range(0,5):
            users.append(User.objects.get(username=f'username${i}'))

        for i in range(1,5):
            users[i].follow(users[0])

        users[1].unfollow(users[0])
        users[2].unfollow(users[0])

        # some redundancy
        users[1].unfollow(users[0])
        users[1].unfollow(users[0])

        self.assertEqual(users[0].followers.all().count(), 2)