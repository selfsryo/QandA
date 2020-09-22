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
