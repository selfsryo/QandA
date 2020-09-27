from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory

from qa.models import Question, Answer
from users.tests.factories import UserFactory
from .factories import QuestionFactory, AnswerFactory


UserModel = get_user_model()

class QuestionManagerTests(TestCase):

    def setUp(self):
        self.user = UserFactory.create()
        # self.users = UserFactory.create_batch(10)
        self.request = RequestFactory()
        self.request.user = self.user
        # import pdb; pdb.set_trace()
        self.q1 = QuestionFactory.create(is_public=True, title='search')
        self.q2 = QuestionFactory.create(is_public=False, text='queryset')
        self.q3 = QuestionFactory.create(is_public=True, author=self.user)

    def test_question_manager_public(self):
        questions = Question.objects.public()
        self.assertEqual(len(questions), 2)

    def test_question_manager_private(self):
        questions = Question.objects.private(self.request)
        self.assertEqual(len(questions), 1)

    def test_question_manager_search(self):
        questions = Question.objects.search('search')
        self.assertEqual(len(questions), 1)

        questions = Question.objects.search('queryset')
        self.assertEqual(len(questions), 1)


class QuestionModelTests(TestCase):

    def setUp(self):
        self.q = QuestionFactory.create()
        self.a = AnswerFactory.create(question=self.q)

    def test_select_best_answer(self):
        self.q.sellect_best(self.a)
        self.assertEqual(self.q.best_answer, self.a)
        self.assertTrue(self.a.is_best)

    def test_leave_best_answer(self):
        self.q.sellect_best(self.a)
        self.q.leave_best()
        self.assertEqual(self.q.best_answer, None)
        self.assertFalse(self.a.is_best)

    def test_update_status_accepted(self):
        self.q.sellect_best(self.a)
        self.q.update_status()
        self.assertEqual(self.q.status, 'accepted')

    def test_update_status_active(self):
        self.q.sellect_best(self.a)
        self.q.leave_best()
        self.q.update_status()
        self.assertEqual(self.q.status, 'active')

    def test_update_status_not_answered(self):
        self.a.delete()
        self.q.update_status()
        self.assertEqual(self.q.status, 'not_answered')


class AnswerManagerTests(TestCase):

    def setUp(self):
        self.q = QuestionFactory.create()
        self.a1 = AnswerFactory.create()
        self.a2 = AnswerFactory.create(is_best=True)
        self.a3 = AnswerFactory.create()

    def test_answer_manager_get_not_best(self):
        answers = Answer.objects.get_not_best()
        self.assertEqual(len(answers), 2)
