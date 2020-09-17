from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.utils import timezone
from datetime import datetime


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        if not email:
            raise ValueError('The given email must be set')
        user = self.model(username=username, 
                          email=self.normalize_email(email),
                          **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)
    
    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField("名前", 
                                unique=True,
                                max_length=20,
                                help_text='20字以内にしてください。')
    email = models.EmailField("メールアドレス", unique=True)
    thumbnail = models.ImageField("サムネイル", 
                                  upload_to=datetime.now().strftime('users/%Y/%m/%d'),
                                  blank=True,
                                  null=True)
    followees = models.ManyToManyField('self',
                                      blank=True,
                                      symmetrical=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)	
    
    objects = UserManager()	
    
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username']	

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'	

    def follow(self, followee):
        self.followees.add(followee)

    def unfollow(self, followee):
        self.followees.remove(followee)
