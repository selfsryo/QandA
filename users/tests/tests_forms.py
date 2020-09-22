from django.test import TestCase
from ..forms import CustomUserCreationForm


class SignUpFormTest(TestCase):
    def test_form_has_fields(self):
        form = CustomUserCreationForm()
        expected = ['username', 'email', 'thumbnail', 'password1', 'password2',]
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)
