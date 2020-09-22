from django.contrib.auth import get_user_model, login, views as auth_views
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.shortcuts import redirect
from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from ..forms import CustomUserCreationForm
from .. import views

UserModel = get_user_model()


class UserDetailTests(TestCase):
    def setUp(self):
        url = reverse('users:signup')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)


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
        self.url = f"/users/detail/{data['username']}/"

    def test_redirection(self):
        self.assertRedirects(self.response, self.url)

    def test_user_creation(self):
        self.assertTrue(UserModel.objects.exists())

    def test_user_authentication(self):
        response = self.client.get(self.url)
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


class UserLoginTests(TestCase):
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


class PasswordResetMailTests(TestCase):
    fixtures = ['active_users']

    def setUp(self):
        self.response = self.client.post(reverse('users:password_reset'), { 'email': 'selfsryo@example.com' })
        self.email = mail.outbox[0]

    def test_email_subject(self):
        self.assertEqual('QAサイト パスワード再登録のお知らせ', self.email.subject)

    def test_email_body(self):
        context = self.response.context
        token = context.get('token')
        uid = context.get('uid')
        password_reset_token_url = reverse('users:password_reset_confirm', kwargs={
            'uidb64': uid,
            'token': token
        })
        self.assertIn(password_reset_token_url, self.email.body)
        self.assertIn('selfsryo', self.email.body)

    def test_email_to(self):
        self.assertEqual(['selfsryo@example.com',], self.email.to)


class PasswordResetTests(TestCase):
    def setUp(self):
        url = reverse('users:password_reset')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/users/password_reset/')
        self.assertEquals(view.func.view_class, views.UserPasswordResetView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PasswordResetForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 2)
        self.assertContains(self.response, 'type="email"', 1)


class SuccessfulPasswordResetTests(TestCase):
    fixtures = ['active_users']

    def setUp(self):
        email = 'selfsryo@example.com'
        url = reverse('users:password_reset')
        self.response = self.client.post(url, {'email': email})

    def test_redirection(self):
        url = reverse('users:password_reset_done')
        self.assertRedirects(self.response, url)

    def test_send_password_reset_email(self):
        self.assertEqual(1, len(mail.outbox))


class InvalidPasswordResetTests(TestCase):
    def setUp(self):
        url = reverse('users:password_reset')
        self.response = self.client.post(url, {'email': 'error@email.com'})

    def test_redirection(self):
        url = reverse('users:password_reset_done')
        self.assertRedirects(self.response, url)

    def test_no_reset_email_sent(self):
        self.assertEqual(0, len(mail.outbox))


class PasswordResetDoneTests(TestCase):
    def setUp(self):
        url = reverse('users:password_reset_done')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/users/password_reset/done/')
        self.assertEquals(view.func.view_class, auth_views.PasswordResetDoneView)


class PasswordResetConfirmTests(TestCase):
    fixtures = ['active_users']

    def setUp(self):
        user = UserModel.objects.get(pk=1)
        # self.uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
        self.uid = urlsafe_base64_encode(force_bytes(user.pk))
        self.token = default_token_generator.make_token(user)

        url = reverse('users:password_reset_confirm', kwargs={'uidb64': self.uid, 'token': self.token})
        self.response = self.client.get(url, follow=True)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve(f'/users/password_reset/{self.uid}/{self.token}/')
        self.assertEquals(view.func.view_class, views.UserPasswordResetConfirmView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SetPasswordForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 3)
        self.assertContains(self.response, 'type="password"', 2)


class PasswordResetCompleteTests(TestCase):
    def setUp(self):
        url = reverse('users:password_reset_complete')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/users/password_reset/complete/')
        self.assertEquals(view.func.view_class, auth_views.PasswordResetCompleteView)
