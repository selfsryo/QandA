from django.conf import settings
from django.utils import timezone
import pytz

from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyInteger, FuzzyText, FuzzyChoice, FuzzyDateTime
from factory import post_generation, SubFactory

from users.tests.factories import UserFactory
from qa.models import Question, Answer, Reply


tzinfo = pytz.timezone(settings.TIME_ZONE)


class QuestionFactory(DjangoModelFactory):
    class Meta:
        model = Question

    title = FuzzyText(prefix='title_', length=10)
    text = FuzzyText(prefix='text_', length=30)
    author = SubFactory(UserFactory)
    created_at = FuzzyDateTime(start_dt=timezone.datetime(2020, 1, 1, tzinfo=tzinfo))
    is_public = FuzzyChoice(choices=[True, False])
    status =  FuzzyChoice(choices=['active', 'not_answered', 'accepted'])

    @post_generation
    def tag(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for tag in extracted:
                self.tag.add(tag)


class AnswerFactory(DjangoModelFactory):
    class Meta:
        model = Answer

    text = FuzzyText(prefix='text_', length=30)
    question = SubFactory(QuestionFactory)
    author = SubFactory(UserFactory)
    created_at = FuzzyDateTime(start_dt=timezone.datetime(2020, 1, 1, tzinfo=tzinfo))


class ReplyFactory(DjangoModelFactory):
    class Meta:
        model = Reply

    text = FuzzyText(prefix='text_', length=30)
    answer = SubFactory(AnswerFactory)
    author = SubFactory(UserFactory)
    created_at = FuzzyDateTime(start_dt=timezone.datetime(2020, 1, 1, tzinfo=tzinfo))
