import datetime
import pytz
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone

from factory import LazyAttribute, post_generation, Sequence
from factory.django import DjangoModelFactory, ImageField
from factory.fuzzy import FuzzyDateTime


tzinfo = pytz.timezone(settings.TIME_ZONE)
UserModel = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = UserModel

    username = Sequence(lambda n: f'user{n}')
    email = LazyAttribute(lambda o: f'{o.username}@example.com')
    thumbnail = ImageField()
    is_staff = False
    is_active = True
    date_joined = FuzzyDateTime(start_dt=timezone.datetime(2020, 1, 1, tzinfo=tzinfo))

    @post_generation
    def followees(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for user in extracted:
                self.followees.add(user)
