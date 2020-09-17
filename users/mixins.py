from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import UserPassesTestMixin


class OnlyYouMixin(UserPassesTestMixin):
	"""本人のみ許可"""
	raise_exception = True

	def test_func(self):
		return self.get_object() == self.request.user


class LoginAndOtherRequiredMixin(UserPassesTestMixin):
	"""ログイン済みかつ本人以外を許可"""
	raise_exception = True

	def test_func(self):
		user = self.request.user
		return user.is_authenticated and user != self.get_object()
