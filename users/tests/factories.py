from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
import pytz

from factory import Sequence
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyInteger, FuzzyText, FuzzyDateTime


tzinfo = pytz.timezone(settings.TIME_ZONE)
UserModel = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = UserModel

    username = Sequence(lambda n: f'user{n}')
    email = Sequence(lambda n: f'mail{n}.example.com')
    is_staff = False
    is_active = True
    date_joined = FuzzyDateTime(start_dt=timezone.datetime(2020, 1, 1, tzinfo=tzinfo))
