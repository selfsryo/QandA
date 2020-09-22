from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyInteger, FuzzyText, FuzzyChoice

from qa.models import Question

# class QuestionFactory(DjangoModelFactory):

#     class Meta:
#         model = Question

#     title = FuzzyText(prefix='title_', length=10)
#     text = FuzzyText(prefix='text_', length=30)
#     is_public = FuzzyChoice(choices=[True, False])
