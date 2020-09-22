from django.contrib.auth import get_user_model
from django.test import TransactionTestCase

UserModel = get_user_model()


class UserModelTests(TransactionTestCase):
    fixtures = ['active_users']

    def test_delete_account(self):
        selfsryo = UserModel.objects.get(pk=1)
        selfsryo.delete()
        self.assertEqual(len(UserModel.objects.all()), 2)

    def test_delete_account2(self):
        selfs = UserModel.objects.get(pk=1)
        selfs.delete()
        self.assertEqual(len(UserModel.objects.all()), 2)

    def test_follow(self):
        user1 = UserModel.objects.get(pk=1)
        user2 = UserModel.objects.get(pk=2)
        user1.follow(user2)
        self.assertTrue(user2 in user1.followees.all())

    def test_unfollow(self):
        user1 = UserModel.objects.get(pk=1)
        user2 = UserModel.objects.get(pk=2)
        user1.follow(user2)
        user1.unfollow(user2)
        self.assertFalse(user2 in user1.followees.all())

