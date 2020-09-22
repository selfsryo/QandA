from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from qa.models import Question

UserModel = get_user_model()


class QuestionManagerTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = UserModel.objects.create_user(
            username='selfsryo',
            email='selfsryo@example.com',
            password='secret')


    def test_public_question_manager(self):
        Question.objects.create(title="title1", text="text1", author=self.user, is_public=True)
        Question.objects.create(title="title2", text="text2", author=self.user, is_public=False)
        Question.objects.create(title="title3", text="text3", author=self.user, is_public=True)

        questions = Question.objects.public()
        self.assertEqual(len(questions), 2)

    # def test_private_question_manager(self):
    #     Question.objects.create(title="title1", text="text1", author=self.request.user, is_public=True)
    #     Question.objects.create(title="title2", text="text2", author=self.request.user, is_public=False)
    #     Question.objects.create(title="title3", text="text3", author=self.request.user, is_public=True)

    #     request = 
    #     questions = Question.objects.private()
    #     self.assertEqual(len(questions), 2)
