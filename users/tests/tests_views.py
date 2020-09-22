from django.contrib.auth import get_user_model, login, views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.shortcuts import redirect

from ..forms import CustomUserCreationForm
from .. import views

UserModel = get_user_model()

class UserSignUpTests(TestCase):
    def setUp(self):
        url = reverse('users:signup')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        view = resolve('/users/signup/')
        self.assertEquals(view.func.view_class, views.UserSignUpView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, CustomUserCreationForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 6)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="file"', 1)
        self.assertContains(self.response, 'type="password"', 2)


class SuccessfulSignUpTests(TestCase):
    def setUp(self):
        url = reverse('users:signup')
        data = {
            'username': 'selfsryo',
            'email': 'selfsryo@example.com',
            'password1': 'secure-pass-selfsryo',
            'password2': 'secure-pass-selfsryo'
        }
        self.response = self.client.post(url, data)
        self.redirect_url = f"/users/detail/{data['username']}/"

    def test_redirection(self):
        self.assertRedirects(self.response, self.redirect_url)

    def test_user_creation(self):
        self.assertTrue(UserModel.objects.exists())

    def test_user_authentication(self):
        response = self.client.get(self.redirect_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class InvalidSignUpTests(TestCase):
    def setUp(self):
        url = reverse('users:signup')
        self.response = self.client.post(url, {})

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_dont_create_user(self):
        self.assertFalse(UserModel.objects.exists())


class UserLoginTest(TestCase):
    fixtures = ['active_users']

    def test_top_page_status_code(self):
        response = Client().get("/users/login/")
        self.assertEqual(200, response.status_code)

    def test_login_success(self):
        user = UserModel.objects.get(pk=1)
        user.set_password('12345')
        user.save()
        logged_in = Client().login(email='selfsryo@example.com', password='12345')
        self.assertTrue(logged_in)

    def test_login_email_error(self):
        user = UserModel.objects.get(pk=1)
        user.set_password('12345')
        user.save()
        logged_in = Client().login(email='error@example.com', password='12345')
        self.assertFalse(logged_in)

    def test_login_password_error(self):
        user = UserModel.objects.get(pk=1)
        user.set_password('12345')
        user.save()
        logged_in = Client().login(email='selfsryo@example.com', password='error')
        self.assertFalse(logged_in)


class PasswordChangeDoneTests(TestCase):
    def setUp(self):
        url = reverse('users:password_change_done')
        self.response = self.client.get(url)

    def test_view_function(self):
        view = resolve('/users/password/done/')
        self.assertEquals(view.func.view_class, auth_views.PasswordChangeDoneView)


class PasswordResetDoneTests(TestCase):
    def setUp(self):
        url = reverse('users:password_reset_done')
        self.response = self.client.get(url)

    def test_view_function(self):
        view = resolve('/users/password_reset/done/')
        self.assertEquals(view.func.view_class, auth_views.PasswordResetDoneView)


class PasswordResetCompleteTests(TestCase):
    def setUp(self):
        url = reverse('users:password_reset_complete')
        self.response = self.client.get(url)

    def test_view_function(self):
        view = resolve('/users/password_reset/complete/')
        self.assertEquals(view.func.view_class, auth_views.PasswordResetCompleteView)
