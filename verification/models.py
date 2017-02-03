from __future__ import unicode_literals

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator

from django.db import models


class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have a valid email address.')

        if not kwargs.get('phone_number'):
            raise ValueError('Users must have a valid phone number.')

        if not kwargs.get('full_name'):
            raise ValueError('Users must have a valid name.')

        account = self.model(
            email=self.normalize_email(email), full_name=kwargs.get('full_name'), phone_number=
            kwargs.get('phone_number')
        )

        account.set_password(password)
        account.save()

        return account


class Account(AbstractBaseUser):
    email = models.EmailField(unique=True)

    full_name = models.CharField(max_length=40, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. "
                                         "Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], blank=False)  # validators should be a list

    password = models.CharField(max_length=8, blank=False);

    is_valid = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'phone_number']

    def __unicode__(self):
        return self.email
