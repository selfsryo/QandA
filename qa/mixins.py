from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import UserPassesTestMixin


class AuthorRequiredMixin(UserPassesTestMixin):
	"""ユーザ-が作成者なら許可"""
	raise_exception = True

	def test_func(self):
		obj = self.get_object()
		author = obj.author
		return author == self.request.user


class PublicOrAuthorRequiredMixin(UserPassesTestMixin):
	"""その質問が公開中、またはユーザ-が質問者なら許可"""
	raise_exception = True

	def test_func(self):
		question = self.get_object()
		return question.is_public or self.request.user == question.author
